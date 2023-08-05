// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef TARGET_DWA2002521_HPP
# define TARGET_DWA2002521_HPP

namespace boost { namespace python { namespace detail {

template<class F>
struct target;

template<class Return>
struct target<Return()> {
    using type = void;
};

template<class Return, class A0, class... Args>
struct target<Return (*)(A0, Args...)> {
    using type = A0&;
};

template<class Return, class Class, class... Args>
struct target<Return (Class::*)(Args...)> {
    using type = Class&;
};
template<class Return, class Class, class... Args>
struct target<Return (Class::*)(Args...) const> {
    using type = Class&;
};
template<class Return, class Class, class... Args>
struct target<Return (Class::*)(Args...) volatile> {
    using type = Class&;
};
template<class Return, class Class, class... Args>
struct target<Return (Class::*)(Args...) const volatile> {
    using type = Class&;
};

template<class Return, class Class>
struct target<Return (Class::*)> {
    using type = Class&;
};

// If F is a function pointer, return the type of the first parameter.
// If F is a member pointer, return the class type.
template<class F>
using target_t = typename target<F>::type;

}}} // namespace boost::python::detail

#endif // TARGET_DWA2002521_HPP
