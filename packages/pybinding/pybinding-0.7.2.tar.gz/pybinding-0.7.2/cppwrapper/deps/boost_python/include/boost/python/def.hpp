// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef DEF_DWA200292_HPP
# define DEF_DWA200292_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/object_fwd.hpp>
# include <boost/python/make_function.hpp>
# include <boost/python/detail/def_helper.hpp>
# include <boost/python/detail/overloads_fwd.hpp>
# include <boost/python/scope.hpp>
# include <boost/python/signature.hpp>
# include <boost/python/detail/scope.hpp>

namespace boost { namespace python {

namespace detail
{
  // Use a def_helper to define a regular wrapped function in the current scope.
  template<class Function, class Helper>
  void def_from_helper(char const* name, Function const& fn, Helper const& h) {
      static_assert(!Helper::has_default_implementation,
                    "Default implementations can only be used with method definitions");
      
      scope_setattr_doc(name, python::make_function(fn, h.policies(), h.keywords()), h.doc());
  }

  // These two overloads discriminate between def() as applied to
  // regular functions and def() as applied to the result of
  // BOOST_PYTHON_FUNCTION_OVERLOADS(). The final argument is used to
  // discriminate.
  template<class Function, class A1>
  void def_maybe_overloads(char const* name, Function f, A1 const& a1,
                           ...)
  {
      def_from_helper(name, f, make_def_helper(a1));
  }

  template<class Function, class Overloads>
  void def_maybe_overloads(char const* name, Function, Overloads const& overloads,
                           overloads_base const*)
  {
      scope current;
      define_with_defaults<get_signature_t<Function>>(name, overloads, current);
  }
}

template<class Function>
void def(char const* name, Function f) {
    detail::scope_setattr_doc(name, make_function(f), nullptr);
}

template<class Function, class MaybeOverloads>
void def(char const* name, Function f, MaybeOverloads const& mo) {
    detail::def_maybe_overloads(name, f, mo, &mo);
}

template <class F, class A1, class A2>
void def(char const* name, F f, A1 const& a1, A2 const& a2) {
    detail::def_from_helper(name, f, detail::make_def_helper(a1, a2));
}

template <class F, class A1, class A2, class A3>
void def(char const* name, F f, A1 const& a1, A2 const& a2, A3 const& a3) {
    detail::def_from_helper(name, f, detail::make_def_helper(a1, a2, a3));
}

}} // namespace boost::python

#endif // DEF_DWA200292_HPP
