// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef MAKE_FUNCTION_DWA20011221_HPP
# define MAKE_FUNCTION_DWA20011221_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/default_call_policies.hpp>
# include <boost/python/args.hpp>
# include <boost/python/signature.hpp>

# include <boost/python/detail/caller.hpp>

# include <boost/python/object/function_object.hpp>

namespace boost { namespace python {

namespace detail
{
  // make_function_aux --
  //
  // These helper functions for make_function (below) do the raw work
  // of constructing a Python object from some invokable entity. See
  // <boost/python/detail/caller.hpp> for more information about how
  // the Sig arguments is used.
  template<class Signature, class CallPolicies, class Function>
  object make_function_aux(Function f, CallPolicies const& cp) {
      return objects::function_object(detail::caller<Function, CallPolicies, Signature>{f, cp});
  }

  // As above, except that it accepts argument keywords. NumKeywords
  // is used only for a compile-time assertion to make sure the user
  // doesn't pass more keywords than the function can accept. To
  // disable all checking, pass 0 for NumKeywords.
  template<class Signature, int NumKeywords, class CallPolicies, class Function>
  object make_function_aux(Function f, CallPolicies const& cp, detail::keyword_range const& kw) {
      static_assert(NumKeywords <= Signature::size - 1, "More keywords than function arguments");

      return objects::function_object(detail::caller<Function, CallPolicies, Signature>{f, cp}, kw);
  }

  //   Helpers for make_function when called with 3 arguments.  These
  //   dispatch functions are used to discriminate between the cases
  //   when the 3rd argument is keywords or when it is a signature.
  template<class CallPolicies, class Keywords, class Function>
  object make_function_dispatch(Function f, CallPolicies const& cp, Keywords const& kw, std::true_type) {
      return detail::make_function_aux<detail::get_signature_t<Function>, Keywords::size>(
          f, cp, kw.range()
      );
  }

  template<class Signature, class CallPolicies, class Function>
  object make_function_dispatch(Function f, CallPolicies const& cp, Signature const&, std::false_type) {
      return detail::make_function_aux<Signature>(f, cp);
  }
}

//   These overloaded functions wrap a function or member function
//   pointer as a Python object, using optional CallPolicies,
//   Keywords, and/or Signature.
//
template<class Function>
object make_function(Function f) {
    return detail::make_function_aux<detail::get_signature_t<Function>>(f, default_call_policies{});
}

template<class Function, class CallPolicies>
object make_function(Function f, CallPolicies const& cp) {
    return detail::make_function_aux<detail::get_signature_t<Function>>(f, cp);
}

template <class Function, class CallPolicies, class KeywordsOrSignature>
object make_function(Function f, CallPolicies const& cp, KeywordsOrSignature const& kw_or_sig) {
    return detail::make_function_dispatch(
        f, cp, kw_or_sig, detail::is_keywords<KeywordsOrSignature>{}
    );
}

template <class Function, class CallPolicies, class Keywords, class Signature>
object make_function(Function f, CallPolicies const& cp, Keywords const& kw, Signature const&) {
    return detail::make_function_aux<Signature, Keywords::size>(
          f, cp, kw.range()
    );
}

// Just pass through if it's already a python object.
inline object make_function(object const& x, ...) { return x; }

}} // namespace boost::python

#endif // MAKE_FUNCTION_DWA20011221_HPP
