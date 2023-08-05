// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#include <boost/python/object/inheritance.hpp>
#include <tuple>
#include <algorithm>
#include <vector>
#include <queue>
#include <cstdint>

//
// Procedure:
//
//      The search is a BFS over the space of (type,address) pairs
//      guided by the edges of the casting graph whose nodes
//      correspond to classes, and whose edges are traversed by
//      applying associated cast functions to an address. We use
//      vertex distance to the goal node in the cast_graph to rate the
//      paths. The vertex distance to any goal node is calculated on
//      demand and outdated by the addition of edges to the graph.

namespace boost { namespace python { namespace objects {

namespace
{
  template <class T> inline void unused_variable(const T&) { }

  struct graph {
      using vertex_t = int;
      struct edge_t {
          vertex_t target;
          cast_function cast;
      };
      using adjacency_list = std::vector<std::vector<edge_t>>;

      // Return a map of the distances from any node to the given target node
      std::vector<int>::const_iterator distances_to(vertex_t target) const {
          const auto n = edges.size();
          if (m_distances.size() != n * n)
              m_distances.resize(n * n, -1);

          auto to_target = m_distances.begin() + n * target;

          // this node hasn't been used as a target yet
          if (to_target[target] != 0) {
              auto reversed = reversed_edges();
              auto queue = std::vector<vertex_t>{target};
              auto next_queue = std::vector<vertex_t>{};

              auto distance = 0;
              while (!queue.empty()) {
                  for (auto vertex_id : queue) {
                      if (to_target[vertex_id] >= 0)
                          continue; // distance already set

                      for (const auto &edge : reversed[vertex_id])
                          next_queue.push_back(edge.target);

                      to_target[vertex_id] = distance;
                  }

                  ++distance;
                  std::swap(queue, next_queue);
                  next_queue.clear();
              }
          }

          return to_target;
      }

      vertex_t add_vertex() {
          edges.emplace_back();
          return static_cast<vertex_t>(edges.size() - 1);
      }

      void add_edge(vertex_t src, vertex_t dst, cast_function cast) {
          edges[src].push_back({dst, cast});
      }

      std::vector<edge_t> const& out_edges(vertex_t target) const {
          return edges[target];
      }

  private:
      adjacency_list reversed_edges() const {
          auto reversed = adjacency_list(edges.size());
          auto const num_edges = static_cast<vertex_t>(edges.size());
          for (vertex_t src = 0; src < num_edges; ++src) {
              for (auto edge : edges[src]) {
                  auto dst = edge.target;
                  edge.target = src;
                  reversed[dst].push_back(edge);
              }
          }

          return reversed;
      }

  private:
      adjacency_list edges;
      mutable std::vector<int> m_distances;
  };
  
  graph& full_graph()
  {
      static graph x;
      return x;
  }
  
  graph& up_graph()
  {
      static graph x;
      return x;
  }

  //
  // Our index of class types
  //
  using index_entry = std::tuple<
      class_id,            // static type
      graph::vertex_t,            // corresponding vertex
      dynamic_id_function  // dynamic_id if polymorphic, or 0
  >;
  enum { ksrc_static_t, kvertex, kdynamic_id };
  using type_index_t = std::vector<index_entry>;

  type_index_t& type_index()
  {
      static type_index_t x;
      return x;
  }

  // map a type to a position in the index
  inline type_index_t::iterator type_position(class_id type)
  {
    return std::find_if(
        type_index().begin(), type_index().end(), 
        [&type](index_entry const& entry) {
            return std::get<ksrc_static_t>(entry) >= type;
        }
    );
  }

  inline index_entry* seek_type(class_id type)
  {
      type_index_t::iterator p = type_position(type);
      if (p == type_index().end() || std::get<ksrc_static_t>(*p) != type)
          return nullptr;
      else
          return &*p;
  }
  
  // Get the entry for a type, inserting if necessary
  inline type_index_t::iterator demand_type(class_id type)
  {
      type_index_t::iterator p = type_position(type);
      if (p != type_index().end() && std::get<ksrc_static_t>(*p) == type)
          return p;

      auto vertex_id = full_graph().add_vertex();
      auto vertex_id2 = up_graph().add_vertex();
      unused_variable(vertex_id2);
      assert(vertex_id == vertex_id2);
      return type_index().insert(p, std::make_tuple(type, vertex_id, dynamic_id_function{nullptr}));
  }

  // Map a two types to a vertex in the graph, inserting if necessary
  inline std::pair<type_index_t::iterator, type_index_t::iterator>
      demand_types(class_id t1, class_id t2)
  {
      // be sure there will be no reallocation
      type_index().reserve(type_index().size() + 2);
      type_index_t::iterator first = demand_type(t1);
      type_index_t::iterator second = demand_type(t2);
      if (first == second)
          ++first;
      return std::make_pair(first, second);
  }

  struct q_elt
  {
      int distance;
      void* src_address;
      graph::vertex_t target;
      cast_function cast;

      bool operator<(q_elt const& rhs) const
      {
          return distance < rhs.distance;
      }
  };

  // Optimization:
  //
  // Given p, src_t, dst_t
  //
  // Get a pointer pd to the most-derived object
  //    if it's polymorphic, dynamic_cast to void*
  //    otherwise pd = p
  //
  // Get the most-derived typeid src_td
  //
  // ptrdiff_t offset = p - pd
  //
  // Now we can keep a cache, for [src_t, offset, src_td, dst_t] of
  // the cast transformation function to use on p and the next src_t
  // in the chain.  src_td, dst_t don't change throughout this
  // process. In order to represent unreachability, when a pair is
  // found to be unreachable, we stick a 0-returning "dead-cast"
  // function in the cache.
  
  // This is needed in a few places below
  inline void* identity_cast(void* p)
  {
      return p;
  }

  void* search(graph const& g, void* p, graph::vertex_t src, graph::vertex_t dst)
  {
      auto d = g.distances_to(dst);
      if (d[src] < 0)
          return nullptr;

      using search_state = std::pair<graph::vertex_t, void*>;
      auto visited = std::vector<search_state>{};
      auto q = std::priority_queue<q_elt>{};
      
      q.push({d[src], p, src, identity_cast});
      while (!q.empty())
      {
          q_elt top = q.top();
          q.pop();
          
          // Check to see if we have a real state
          void* dst_address = top.cast(top.src_address);
          if (dst_address == nullptr)
              continue;

          if (top.target == dst)
              return dst_address;
          
          search_state s(top.target,dst_address);

          auto pos = std::lower_bound(
              visited.begin(), visited.end(), s);

          // If already visited, continue
          if (pos != visited.end() && *pos == s)
              continue;
          
          visited.insert(pos, s); // mark it

          // expand it:
          const auto& edges = g.out_edges(s.first);
          for (const auto& edge : edges) {
              q.push({d[edge.target], dst_address, edge.target, edge.cast});
          }
      }
      return nullptr;
  }

  struct cache_element
  {
      using key_type = std::tuple<
          class_id,           // source static type
          class_id,           // target type
          std::ptrdiff_t,     // offset within source object
          class_id            // source dynamic type
      >;

      cache_element(key_type const& k)
          : key(k)
          , offset(0)
      {}
      
      key_type key;
      std::ptrdiff_t offset;

      static constexpr std::ptrdiff_t not_found = PTRDIFF_MIN;
      
      bool operator<(cache_element const& rhs) const
      {
          return this->key < rhs.key;
      }

      bool unreachable() const
      {
          return offset == not_found;
      }
  };
  
  enum { kdst_t = ksrc_static_t + 1, koffset, ksrc_dynamic_t };
  using cache_t = std::vector<cache_element>;

  cache_t& cache()
  {
      static cache_t x;
      return x;
  }

  inline void* convert_type(void* const p, class_id src_t, class_id dst_t, bool polymorphic)
  {
      // Quickly rule out unregistered types
      index_entry* src_p = seek_type(src_t);
      if (src_p == 0)
          return 0;

      index_entry* dst_p = seek_type(dst_t);
      if (dst_p == 0)
          return 0;
    
      // Look up the dynamic_id function and call it to get the dynamic
      // info
      boost::python::objects::dynamic_id_t dynamic_id = polymorphic
          ? std::get<kdynamic_id>(*src_p)(p)
          : std::make_pair(p, src_t);
    
      // Look in the cache first for a quickie address translation
      std::ptrdiff_t offset = (char*)p - (char*)dynamic_id.first;

      cache_element seek(std::make_tuple(src_t, dst_t, offset, dynamic_id.second));
      cache_t& c = cache();
      cache_t::iterator const cache_pos
          = std::lower_bound(c.begin(), c.end(), seek);
                      

      // if found in the cache, we're done
      if (cache_pos != c.end() && cache_pos->key == seek.key)
      {
          return cache_pos->offset == cache_element::not_found
              ? 0 : (char*)p + cache_pos->offset;
      }

      // If we are starting at the most-derived type, only look in the up graph
      graph const& g = polymorphic && dynamic_id.second != src_t
          ? full_graph() : up_graph();
    
      void* result = search(
          g, p, std::get<kvertex>(*src_p)
          , std::get<kvertex>(*dst_p));

      // update the cache
      c.insert(cache_pos, seek)->offset
          = (result == 0) ? cache_element::not_found : (char*)result - (char*)p;

      return result;
  }
} // end anonymous namespace

BOOST_PYTHON_DECL void* find_dynamic_type(void* p, class_id src_t, class_id dst_t)
{
    return convert_type(p, src_t, dst_t, true);
}

BOOST_PYTHON_DECL void* find_static_type(void* p, class_id src_t, class_id dst_t)
{
    return convert_type(p, src_t, dst_t, false);
}

BOOST_PYTHON_DECL void add_cast(
    class_id src_t, class_id dst_t, cast_function cast, bool is_downcast)
{
    // adding an edge will invalidate any record of unreachability in
    // the cache.
    static std::size_t expected_cache_len = 0;
    cache_t& c = cache();
    if (c.size() > expected_cache_len)
    {
        c.erase(std::remove_if(
                    c.begin(), c.end(),
                    [](cache_element const& e) { return e.unreachable(); })
                , c.end());

        // If any new cache entries get added, we'll have to do this
        // again when the next edge is added
        expected_cache_len = c.size();
    }
    
    auto types = demand_types(src_t, dst_t);
    auto src = std::get<kvertex>(*types.first);
    auto dst = std::get<kvertex>(*types.second);

    full_graph().add_edge(src, dst, cast);
    if (!is_downcast)
        up_graph().add_edge(src, dst, cast);
}

BOOST_PYTHON_DECL void register_dynamic_id_aux(
    class_id static_id, dynamic_id_function get_dynamic_id)
{
    std::get<kdynamic_id>(*demand_type(static_id)) = get_dynamic_id;
}

}}} // namespace boost::python::objects
