// Copyright David Abrahams 2005.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef IS_XXX_DWA2003224_HPP
# define IS_XXX_DWA2003224_HPP

namespace boost { namespace python { namespace detail { 

//
//  Test for any kind of template type. 
//
//  E.g.: "is_<shared_ptr, T>::value" will return true
//        if "T == shared_ptr<U>" where U is anything.
//

template<template<class...> class Class, class T>
struct is_ : std::false_type {};

template<template<class...> class Class, class... Args>
struct is_<Class, Class<Args...>> : std::true_type {};

//
//  Test if a template is the base of T.
//
//  E.g.: "is_base_template_of<Class, T>::value" will return true
//        if T is derived from Class<U> where U is anything.
//

template<template<class...> class Class, class T>
struct is_base_template_of {
    template<class... Args>
    static std::true_type is_convertible(Class<Args...>*);
    static std::false_type is_convertible(...);

    using type = decltype(is_convertible(std::declval<T*>()));
    static constexpr bool value = type::value;
};

}}} // namespace boost::python::detail

#endif // IS_XXX_DWA2003224_HPP
