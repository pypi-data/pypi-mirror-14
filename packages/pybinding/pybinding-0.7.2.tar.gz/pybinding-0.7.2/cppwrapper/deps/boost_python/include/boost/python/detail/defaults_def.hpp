///////////////////////////////////////////////////////////////////////////////
//
// Copyright David Abrahams 2002, Joel de Guzman, 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
//
///////////////////////////////////////////////////////////////////////////////
#ifndef DEFAULTS_DEF_JDG20020811_HPP
#define DEFAULTS_DEF_JDG20020811_HPP

#include <boost/python/detail/defaults_gen.hpp>
#include <boost/python/class_fwd.hpp>
#include <boost/python/scope.hpp>
#include <boost/python/detail/scope.hpp>
#include <boost/python/detail/make_keyword_range_fn.hpp>
#include <boost/python/object/add_to_namespace.hpp>
#include <boost/python/detail/type_list_utils.hpp>

///////////////////////////////////////////////////////////////////////////////
namespace boost { namespace python {

struct module;

namespace objects
{
  struct class_base;
}

namespace detail
{
  // Called as::
  //
  //    name_space_def(ns, "func", func, kw, policies, docstring, &ns)
  //
  // Dispatch to properly add f to namespace ns.
  //
  // @group define_stub_function helpers { 
  template <class Func, class CallPolicies, class NameSpaceT>
  static void name_space_def(
      NameSpaceT& name_space
      , char const* name
      , Func f
      , keyword_range const& kw
      , CallPolicies const& policies
      , char const* doc
      , objects::class_base*
      )
  {
      typedef typename NameSpaceT::wrapped_type wrapped_type;
      
      objects::add_to_namespace(
          name_space, name,
          detail::make_keyword_range_function<get_signature_t<Func, wrapped_type>>(f, policies, kw)
        , doc
      );
  }

  template <class Func, class CallPolicies>
  static void name_space_def(
      object& name_space
      , char const* name
      , Func f
      , keyword_range const& kw
      , CallPolicies const& policies
      , char const* doc
      , ...
      )
  {
      scope within(name_space);

      detail::scope_setattr_doc(
          name
          , detail::make_keyword_range_function(f, policies, kw)
          , doc);
  }

  // For backward compatibility -- is this obsolete?
  template <class Func, class CallPolicies, class NameSpaceT>
  static void name_space_def(
      NameSpaceT& name_space
      , char const* name
      , Func f
      , keyword_range const& // ignored
      , CallPolicies const& policies
      , char const* doc
      , module*
      )
  {
      name_space.def(name, f, policies, doc);
  }
  // }

  
  //  This helper template struct does the actual recursive
  //  definition.  There's a generic version
  //  define_with_defaults_helper<N> and a terminal case
  //  define_with_defaults_helper<0>. The struct and its
  //  specialization has a sole static member function def that
  //  expects:
  //
  //    1. char const* name:        function name that will be
  //                                visible to python
  //
  //    2. OverloadsT:              a function overloads struct
  //                                (see defaults_gen.hpp)
  //
  //    3. NameSpaceT& name_space:  a python::class_ or
  //                                python::module instance
  //
  //    4. char const* name:        doc string
  //
  //  The def static member function calls a corresponding
  //  define_stub_function<N>. The general case recursively calls
  //  define_with_defaults_helper<N-1>::def until it reaches the
  //  terminal case case define_with_defaults_helper<0>.
  template <class Overloads, class Sig, int N>
  struct define_with_defaults_helper
  {
      template <class CallPolicies, class NameSpaceT>
      static void
      def(
          char const* name,
          keyword_range kw,
          CallPolicies const& policies,
          NameSpaceT& name_space,
          char const* doc)
      {
          //  define the NTH stub function of stubs
          using gen = typename Overloads::template gen<Sig>;
          detail::name_space_def(name_space, name, &gen::func, kw, policies, doc, &name_space);

          if (kw.second > kw.first)
              --kw.second;

          //  call the next define_with_defaults_helper
          using next_sig = tl::drop_t<Sig, 1>;
          define_with_defaults_helper<Overloads, next_sig, N-1>::def(
              name, kw, policies, name_space, doc
          );
      }
  };

  template <class Overloads, class Sig>
  struct define_with_defaults_helper<Overloads, Sig, 0>
  {
      template <class CallPolicies, class NameSpaceT>
      static void
      def(
          char const* name,
          keyword_range const& kw,
          CallPolicies const& policies,
          NameSpaceT& name_space,
          char const* doc)
      {
          //  define the Oth stub function of stubs
          using gen = typename Overloads::template gen<Sig>;
          detail::name_space_def(name_space, name, &gen::func, kw, policies, doc, &name_space);
      }
  };

  //  define_with_defaults
  //
  //      1. char const* name:        function name that will be
  //                                  visible to python
  //
  //      2. OverloadsT:              a function overloads struct
  //                                  (see defaults_gen.hpp)
  //
  //      3. CallPolicies& policies:  Call policies
  //      4. NameSpaceT& name_space:  a python::class_ or
  //                                  python::module instance
  //
  //      5. SigT sig:                Function signature typelist
  //                                  (see defaults_gen.hpp)
  //
  //      6. char const* name:        doc string
  //
  //  This is the main entry point. This function recursively
  //  defines all stub functions of StubT (see defaults_gen.hpp) in
  //  NameSpaceT name_space which can be either a python::class_ or
  //  a python::module. The sig argument is a typelist that
  //  specifies the return type, the class (for member functions,
  //  and the arguments. Here are some SigT examples:
  //
  //      int foo(int)        type_list<int, int>
  //      void bar(int, int)  type_list<void, int, int>
  //      void C::foo(int)    type_list<void, C, int>
  //
  template<class Signature, class Overloads, class Namespace>
  inline void define_with_defaults(char const* name, Overloads const& overloads, Namespace& ns) {
      using overloads_t = typename Overloads::type;
      static_assert(overloads_t::max_args <= Signature::size, "Too many arguments.");

      define_with_defaults_helper<overloads_t, Signature, overloads_t::n_funcs-1>::def(
          name
          , overloads.keywords()
          , overloads.call_policies()
          , ns
          , overloads.doc_string());
  }

} // namespace detail

}} // namespace boost::python

#endif // DEFAULTS_DEF_JDG20020811_HPP
