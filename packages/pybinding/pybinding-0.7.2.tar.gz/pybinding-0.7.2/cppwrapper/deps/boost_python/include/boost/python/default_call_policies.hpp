// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef DEFAULT_CALL_POLICIES_DWA2002131_HPP
# define DEFAULT_CALL_POLICIES_DWA2002131_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/to_python_value.hpp>
# include <boost/python/detail/value_arg.hpp>
# include <boost/python/detail/type_list_utils.hpp>

namespace boost { namespace python { 

struct default_result_converter;

template<std::size_t offset>
struct offset_args {
    PyObject* base_args;

    PyObject* get(std::size_t n) const {
        return PyTuple_GET_ITEM(base_args, n + offset);
    }

    ssize_t arity() const {
        return PyTuple_GET_SIZE(base_args) - offset;
    }
};

struct default_call_policies {
    // Ownership of this argument tuple will ultimately be adopted by the caller.
    template <class ArgumentPackage>
    static bool precall(ArgumentPackage const&) {
        return true;
    }

    // Pass the result through
    template <class ArgumentPackage>
    static PyObject* postcall(ArgumentPackage const&, PyObject* result) {
        return result;
    }

    using result_converter = default_result_converter;
    using argument_package = offset_args<0>;

    template<class Signature>
    struct extract_return_type {
        using type = detail::tl::front_t<Signature>;
    };

    template<class Signature>
    struct extract_signature {
        using type = Signature;
    };
};

struct default_result_converter {
    template <class R>
    struct apply {
        static_assert(!std::is_pointer<R>::value && !std::is_reference<R>::value,
                      "Specify a return value policy to wrap functions");
        using type = boost::python::make_to_python_value<R>;
    };
};

// Exceptions for c strings an PyObject*s
template <>
struct default_result_converter::apply<char const*> {
    using type = boost::python::to_python_value<char const*>;
};

template <>
struct default_result_converter::apply<PyObject*> {
    using type = boost::python::to_python_value<PyObject*>;
};

}} // namespace boost::python

#endif // DEFAULT_CALL_POLICIES_DWA2002131_HPP
