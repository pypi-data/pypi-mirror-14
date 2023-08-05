// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef OBJECT_OPERATORS_DWA2002617_HPP
# define OBJECT_OPERATORS_DWA2002617_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/object_core.hpp>
# include <boost/python/call.hpp>

# include <boost/python/detail/is_xxx.hpp>

# include <boost/python/cpp14/type_traits.hpp>

namespace boost { namespace python {

namespace detail {
    struct kwargs_proxy {
        explicit kwargs_proxy(object target) : target{target} {}
        operator object() const { return target; }
        PyObject* ptr() const { return target.ptr(); }

    protected:
        object target;
    };

    struct args_proxy : kwargs_proxy {
        using kwargs_proxy::kwargs_proxy;
        kwargs_proxy operator*() const { return kwargs_proxy{target}; }
    };
}

template<class U>
template<class... Args>
object api::object_operators<U>::operator()(Args const&... args) const {
    return call<object>(get_managed_object(this->derived()), args...);
}

template<class U>
detail::args_proxy api::object_operators<U>::operator*() const {
    return detail::args_proxy{this->derived()};
}

template<class U>
object api::object_operators<U>::operator()(detail::args_proxy const& args) const {
    return object{detail::new_reference(
        PyObject_Call(
            get_managed_object(this->derived()),
            args.ptr(),
            nullptr
        )
    )};
};

template<class U>
object api::object_operators<U>::operator()(detail::kwargs_proxy const& kwargs) const {
    return object{detail::new_reference(
        PyObject_Call(
            get_managed_object(this->derived()),
            handle<>{PyTuple_New(0)}.get(),
            kwargs.ptr()
        )
    )};
};

template<class U>
object api::object_operators<U>::operator()(detail::args_proxy const& args,
                                            detail::kwargs_proxy const& kwargs) const
{
    return object{detail::new_reference(
        PyObject_Call(
            get_managed_object(this->derived()),
            args.ptr(),
            kwargs.ptr()
        )
    )};
};

namespace api {

template <class L, class R = L>
struct is_object_operators {
    static constexpr bool value = python::detail::is_base_template_of<object_operators, L>::value
                               || python::detail::is_base_template_of<object_operators, R>::value;
    using type = std::integral_constant<bool, value>;
};

template <class L, class R, class T>
using enable_binary_t = cpp14::enable_if_t<is_object_operators<L,R>::value, T>;

template <class U>
inline object_operators<U>::operator bool_type() const {
    int is_true = PyObject_IsTrue(get_managed_object(this->derived()));
    if (is_true < 0) throw_error_already_set();
    return is_true ? &object::ptr : nullptr;
}

# define BOOST_PYTHON_BINARY_OPERATOR(op)                               \
BOOST_PYTHON_DECL object operator op(object const& l, object const& r); \
template <class L, class R>                                             \
enable_binary_t<L, R, object> operator op(L const& l, R const& r)       \
{                                                                       \
    return object(l) op object(r);                                      \
}
BOOST_PYTHON_BINARY_OPERATOR(>)
BOOST_PYTHON_BINARY_OPERATOR(>=)
BOOST_PYTHON_BINARY_OPERATOR(<)
BOOST_PYTHON_BINARY_OPERATOR(<=)
BOOST_PYTHON_BINARY_OPERATOR(==)
BOOST_PYTHON_BINARY_OPERATOR(!=)
BOOST_PYTHON_BINARY_OPERATOR(+)
BOOST_PYTHON_BINARY_OPERATOR(-)
BOOST_PYTHON_BINARY_OPERATOR(*)
BOOST_PYTHON_BINARY_OPERATOR(/)
BOOST_PYTHON_BINARY_OPERATOR(%)
BOOST_PYTHON_BINARY_OPERATOR(<<)
BOOST_PYTHON_BINARY_OPERATOR(>>)
BOOST_PYTHON_BINARY_OPERATOR(&)
BOOST_PYTHON_BINARY_OPERATOR(^)
BOOST_PYTHON_BINARY_OPERATOR(|)
# undef BOOST_PYTHON_BINARY_OPERATOR

        
# define BOOST_PYTHON_INPLACE_OPERATOR(op)                              \
BOOST_PYTHON_DECL object& operator op(object& l, object const& r);      \
template <class R>                                                      \
object& operator op(object& l, R const& r)                              \
{                                                                       \
    return l op object(r);                                              \
}
BOOST_PYTHON_INPLACE_OPERATOR(+=)
BOOST_PYTHON_INPLACE_OPERATOR(-=)
BOOST_PYTHON_INPLACE_OPERATOR(*=)
BOOST_PYTHON_INPLACE_OPERATOR(/=)
BOOST_PYTHON_INPLACE_OPERATOR(%=)
BOOST_PYTHON_INPLACE_OPERATOR(<<=)
BOOST_PYTHON_INPLACE_OPERATOR(>>=)
BOOST_PYTHON_INPLACE_OPERATOR(&=)
BOOST_PYTHON_INPLACE_OPERATOR(^=)
BOOST_PYTHON_INPLACE_OPERATOR(|=)
# undef BOOST_PYTHON_INPLACE_OPERATOR

}}} // namespace boost::python

#endif // OBJECT_OPERATORS_DWA2002617_HPP
