// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef MAKE_KEYWORD_RANGE_FN_DWA2002927_HPP
# define MAKE_KEYWORD_RANGE_FN_DWA2002927_HPP

# include <boost/python/make_function.hpp>
# include <boost/python/args_fwd.hpp>
# include <boost/python/object/make_holder.hpp>

namespace boost { namespace python { namespace detail { 

// Think of this as a version of make_function without a compile-time
// check that the size of kw is no greater than the expected arity of
// Function. This version is needed when defining functions with default
// arguments, because compile-time information about the number of
// keywords is missing for all but the initial function definition.
template<class CallPolicies, class Function>
object make_keyword_range_function(Function f, CallPolicies const& cp, keyword_range const& kw) {
    return detail::make_function_aux<detail::get_signature_t<Function>, 0>(f, cp, kw);
}

template<class Signature, class CallPolicies, class Function>
object make_keyword_range_function(Function f, CallPolicies const& cp, keyword_range const& kw) {
    return detail::make_function_aux<Signature, 0>(f, cp, kw);
}

// Builds an '__init__' function which inserts the given Holder type
// in a wrapped C++ class instance. Signature is a type_list describing
// the C++ argument types to be passed to Holder's constructor.
template<class Signature, class Holder, class CallPolicies>
object make_keyword_range_constructor(CallPolicies const& cp, detail::keyword_range const& kw) {
    return detail::make_keyword_range_function(
        objects::make_holder<Holder, Signature>::execute,
#ifndef BOOST_PYTHON_NO_PY_SIGNATURES
        objects::holder_policy<typename Holder::value_type, CallPolicies>{cp},
#else
        cp,
#endif
        kw
    );
}

}}} // namespace boost::python::detail

#endif // MAKE_KEYWORD_RANGE_FN_DWA2002927_HPP
