// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef BASE_TYPE_TRAITS_DWA2002614_HPP
# define BASE_TYPE_TRAITS_DWA2002614_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/cpp14/type_traits.hpp>

namespace boost { namespace python { 

template <class T>
struct base_type_traits : std::false_type {};

template<>
struct base_type_traits<PyObject> : std::true_type {};
template<>
struct base_type_traits<PyTypeObject> : std::true_type {};
template<>
struct base_type_traits<PyMethodObject> : std::true_type {};

// Test for PyObject or struct derived from PyObject using C-style inheritance
template<class T>
using is_c_pyobject = base_type_traits<cpp14::remove_cv_t<T>>;

// Test for any kind of PyObject including C++ inheritance
template<class T>
using is_pyobject = std::integral_constant<bool,
    is_c_pyobject<T>::value || std::is_base_of<PyObject, T>::value
>;

}} // namespace boost::python

#endif // BASE_TYPE_TRAITS_DWA2002614_HPP
