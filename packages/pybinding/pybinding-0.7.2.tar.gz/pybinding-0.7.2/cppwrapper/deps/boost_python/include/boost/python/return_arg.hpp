// Copyright David Abrahams and Nikolay Mladenov 2003.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef RETURN_ARG_DWA2003719_HPP
# define RETURN_ARG_DWA2003719_HPP
# include <boost/python/default_call_policies.hpp>
# include <boost/python/detail/none.hpp>
# include <boost/python/detail/value_arg.hpp>

# include <boost/python/refcount.hpp>

namespace boost { namespace python { 

namespace detail {
    struct return_none {
        template <class T>
        struct apply {
            struct type {
                static bool convertible() { return true; }
                PyObject* operator()(value_arg_t<T>) const { return none(); }
            };
        };
    };
}

template<std::size_t arg_pos = 1, class BasePolicy = default_call_policies>
struct return_arg : BasePolicy {
    static_assert(arg_pos > 0, "arg_pos == 0 is the result");
    // We could default to the base result_converter in case of arg_pos == 0
    // since return arg 0 means return result, but I think it is better to
    // issue an error instead, cause it can lead to confusions

    using result_converter = detail::return_none;

    template <class ArgumentPackage>
    static PyObject* postcall(ArgumentPackage const& args, PyObject* result) {
        result = BasePolicy::postcall(args, result);
        if (!result)
            return nullptr;
        decref(result);
        return incref(args.get(arg_pos - 1));
    }

    template<class Signature>
    struct extract_return_type {
        using type = detail::tl::get_t<Signature, arg_pos>;
    };
};

template<class BasePolicy = default_call_policies>
struct return_self : return_arg<1, BasePolicy> {};

}} // namespace boost::python

#endif // RETURN_ARG_DWA2003719_HPP
