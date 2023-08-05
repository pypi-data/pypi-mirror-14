// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef ITERATOR_DWA2002510_HPP
# define ITERATOR_DWA2002510_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/class.hpp>
# include <boost/python/return_value_policy.hpp>
# include <boost/python/return_by_value.hpp>
# include <boost/python/handle.hpp>
# include <boost/python/make_function.hpp>

# include <boost/python/object/iterator_core.hpp>
# include <boost/python/object/class_detail.hpp>
# include <boost/python/object/function_object.hpp>

# include <boost/python/detail/raw_pyobject.hpp>

namespace boost { namespace python { namespace objects {

// CallPolicies for the next() method of iterators. We don't want
// users to have to explicitly specify that the references returned by
// iterators are copied, so we just replace the result_converter from
// the default_iterator_call_policies with a permissive one which
// always copies the result.
typedef return_value_policy<return_by_value> default_iterator_call_policies;

// Instantiations of these are wrapped to produce Python iterators.
template <class NextPolicies, class Iterator>
struct iterator_range
{
    iterator_range(object sequence, Iterator start, Iterator finish);

    using traits_t = std::iterator_traits<Iterator>;

    struct next
    {
        using result_type = cpp14::conditional_t<
            std::is_reference<typename traits_t::reference>::value,
            typename traits_t::reference,
            typename traits_t::value_type
        >;
        
        result_type
        operator()(iterator_range<NextPolicies,Iterator>& self)
        {
            if (self.m_start == self.m_finish)
                stop_iteration_error();
            return *self.m_start++;
        }
    };
    
    typedef next next_fn;
    
    object m_sequence; // Keeps the sequence alive while iterating.
    Iterator m_start;
    Iterator m_finish;
};

namespace detail
{
  // Get a Python class which contains the given iterator and
  // policies, creating it if necessary. Requires: NextPolicies is
  // default-constructible.
  template <class Iterator, class NextPolicies>
  object demand_iterator_class(char const* name, Iterator* = 0, NextPolicies const& policies = NextPolicies())
  {
      typedef iterator_range<NextPolicies,Iterator> range_;

      // Check the registry. If one is already registered, return it.
      handle<> class_obj(
          objects::registered_class_object(python::type_id<range_>()));
        
      if (class_obj.get() != 0)
          return object(class_obj);

      typedef typename range_::next_fn next_fn;
      typedef typename next_fn::result_type result_type;
      
      return class_<range_>(name, no_init)
          .def("__iter__", identity_function())
          .def(
#if PY_VERSION_HEX >= 0x03000000
              "__next__"
#else
              "next"
#endif
            , make_function(
                next_fn()
              , policies
              , python::detail::type_list<result_type,range_&>()
            ));
  }

  // A function object which builds an iterator_range.
  template <
      class Target
    , class Iterator
    , class Accessor1
    , class Accessor2
    , class NextPolicies
  >
  struct py_iter_
  {
      py_iter_(Accessor1 const& get_start, Accessor2 const& get_finish)
        : m_get_start(get_start)
        , m_get_finish(get_finish)
      {}
      
      // Extract an object x of the Target type from the first Python
      // argument, and invoke get_start(x)/get_finish(x) to produce
      // iterators, which are used to construct a new iterator_range<>
      // object that gets wrapped into a Python iterator.
      iterator_range<NextPolicies,Iterator>
      operator()(back_reference<Target&> x) const
      {
          // Make sure the Python class is instantiated.
          detail::demand_iterator_class("iterator", (Iterator*)0, NextPolicies());
          
          return iterator_range<NextPolicies,Iterator>(
              x.source()
            , m_get_start(x.get())
            , m_get_finish(x.get())
          );
      }
   private:
      Accessor1 m_get_start;
      Accessor2 m_get_finish;
  };

  template <class NextPolicies, class Target, class Iterator, class Accessor1, class Accessor2>
  inline object make_iterator_function(
      Accessor1 const& get_start
    , Accessor2 const& get_finish
    , Iterator const& (*)()
  )
  {
      return make_function(
          py_iter_<Target,Iterator,Accessor1,Accessor2,NextPolicies>(get_start, get_finish)
        , default_call_policies()
        , python::detail::type_list<iterator_range<NextPolicies,Iterator>, back_reference<Target&> >()
      );
  }

  template <class NextPolicies, class Target, class Iterator, class Accessor1, class Accessor2>
  inline object make_iterator_function(
      Accessor1 const& get_start
    , Accessor2 const& get_finish
    , Iterator& (*)()
  )
  {
      return make_iterator_function<NextPolicies, Target>(
          get_start
        , get_finish
        , (Iterator const&(*)())0
      );
  }

}

// Create a Python callable object which accepts a single argument
// convertible to the C++ Target type and returns a Python
// iterator. The Python iterator uses get_start(x) and get_finish(x)
// (where x is an instance of Target) to produce begin and end
// iterators for the range, and an instance of NextPolicies is used as
// CallPolicies for the Python iterator's next() function. 
template <class NextPolicies, class Target, class Accessor1, class Accessor2>
inline object make_iterator_function(Accessor1 const& get_start, Accessor2 const& get_finish)
{
    using iterator = cpp14::result_of_t<Accessor1(Target&)>;
    using iterator_const = cpp14::add_const_t<iterator>;
    using iterator_cref = cpp14::add_lvalue_reference_t<iterator_const>;
      
    return detail::make_iterator_function<NextPolicies, Target>(
        get_start
      , get_finish
      , (iterator_cref(*)())0
    );
}

//
// implementation
//
template <class NextPolicies, class Iterator>
inline iterator_range<NextPolicies,Iterator>::iterator_range(
    object sequence, Iterator start, Iterator finish)
    : m_sequence(sequence), m_start(start), m_finish(finish)
{
}

}}} // namespace boost::python::objects

#endif // ITERATOR_DWA2002510_HPP
