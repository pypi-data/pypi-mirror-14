// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef POINTEE_DWA2002323_HPP
# define POINTEE_DWA2002323_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/cpp14/type_traits.hpp>
# include <boost/python/detail/void_t.hpp>

namespace boost { namespace python {

namespace detail {
    // T is a raw pointer or a value type
    template<class T, class = void>
    struct pointee_impl {
        using type = cpp14::remove_pointer_t<T>;
    };

    // T is a smart pointer
    template<class T>
    struct pointee_impl<T, void_t<typename T::element_type>> {
        using type = typename T::element_type;
    };
}

// T is a pointer type
template<class T>
struct pointee : detail::pointee_impl<T> {};

template<class T>
using pointee_t = typename pointee<T>::type;

}} // namespace boost::python::detail

#endif // POINTEE_DWA2002323_HPP
