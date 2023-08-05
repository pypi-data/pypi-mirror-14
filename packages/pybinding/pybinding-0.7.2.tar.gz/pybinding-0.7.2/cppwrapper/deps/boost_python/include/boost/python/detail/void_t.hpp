#pragma once

namespace boost { namespace python { namespace detail {

// This struct is required for compatibility with GCC
template<class...>
struct void_type {
    using type = void;
};

template<class... Ts>
using void_t = typename void_type<Ts...>::type;

}}} // namespace boost::python::detail
