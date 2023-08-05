// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef CALLER_DWA20021121_HPP
# define CALLER_DWA20021121_HPP

# include <boost/python/cpp14/utility.hpp>
# include <boost/python/cpp14/type_traits.hpp>

# include <boost/python/detail/invoke.hpp>
# include <boost/python/detail/signature.hpp>

# include <boost/python/type_id.hpp>
# include <boost/python/converter/arg_from_python.hpp>
# include <boost/python/converter/context_result_converter.hpp>
# include <boost/python/converter/builtin_converters.hpp>

namespace boost { namespace python { namespace detail { 

// A dummy converter is required for void.
template <class CallPolicies, class Result>
struct select_result_converter {
    using type = typename CallPolicies::result_converter::template apply<Result>::type;
};

template <class CallPolicies>
struct select_result_converter<CallPolicies, void> {
    struct type {};
};

template <class CallPolicies, class Result>
using select_result_converter_t = typename select_result_converter<CallPolicies, Result>::type;


template<class ResultConverter>
inline ResultConverter create_result_converter_impl(PyObject* args, std::true_type) {
    return {args};
}

template<class ResultConverter>
inline ResultConverter create_result_converter_impl(PyObject* /*args*/, std::false_type) {
    return {};
}

template<class CallPolicies, class Result,
         class ResultConverter = select_result_converter_t<CallPolicies, Result>>
inline ResultConverter create_result_converter(PyObject* args) {
    using pick = std::is_base_of<converter::context_result_converter, ResultConverter>;
    return create_result_converter_impl<ResultConverter>(args, pick{});
}

// A function object type which wraps C++ objects as Python callable
// objects.
//
// Template Arguments:
//
//   Function -
//      the C++ `function object' that will be called. Might
//      actually be any data for which an appropriate invoke_tag can
//      be generated. invoke(...) takes care of the actual invocation syntax.
//
//   CallPolicies -
//      The precall, postcall, and what kind of resultconverter to
//      generate for Result
//
//   Signature -
//      The `intended signature' of the function. A type_list
//      beginning with a result type and continuing with a list of
//      argument types.
template<class Function, class CallPolicies, class Signature,
         class = cpp14::make_index_sequence<Signature::size - 1>>
class caller;

template<class Function, class CallPolicies, class Result, class... Args, std::size_t... Is>
class caller<Function, CallPolicies, type_list<Result, Args...>, cpp14::index_sequence<Is...>>
    : public CallPolicies // inherit to take advantage of empty base class optimisation
{
    using argument_package = typename CallPolicies::argument_package;
    using signature_t = typename CallPolicies::template extract_signature<
        type_list<Result, Args...>
    >::type;
    using signature_return_t = cpp14::remove_cv_t<cpp14::remove_pointer_t<
        typename CallPolicies::template extract_return_type<signature_t>::type
    >>;

public:
    caller(Function f, CallPolicies const& cp)
        : CallPolicies(cp), m_function(f)
    {
#ifndef BOOST_PYTHON_NO_PY_SIGNATURES
        converter::registry::set_to_python_type(
            type_id<signature_return_t>(),
            to_python_pytype<signature_return_t>::get()
        );
#endif
    }

    PyObject* operator()(PyObject* args, PyObject* /*kwargs*/) {
        auto arg_pack = argument_package{args};
        return call_impl(arg_pack, converter::arg_from_python<Args>(arg_pack.get(Is))...);
    }
    
    static std::size_t min_arity() { return sizeof...(Args); }

    static py_func_sig_info signature() {
        auto sig = detail::signature<signature_t>::elements();

#ifndef BOOST_PYTHON_NO_PY_SIGNATURES
        sig[0] = {
            type_id<signature_return_t>(),
            is_reference_to_non_const<signature_return_t>::value
        };
#endif
        return sig;
    }

private:
    template<class... Converters>
    PyObject* call_impl(argument_package arg_pack, Converters... converters) {
        for (auto is_convertible : {converters.check()..., true}) {
            if (!is_convertible)
                return nullptr;
        }

        if (!CallPolicies::precall(arg_pack))
            return nullptr;

        PyObject* result = detail::invoke(
            detail::make_invoke_tag<Result, Function>{},
            create_result_converter<CallPolicies, Result>(arg_pack.base_args),
            m_function,
            std::move(converters)...
        );

        return CallPolicies::postcall(arg_pack, result);
    }

private:
    Function m_function;
};
    
}}} // namespace boost::python::detail

#endif // CALLER_DWA20021121_HPP
