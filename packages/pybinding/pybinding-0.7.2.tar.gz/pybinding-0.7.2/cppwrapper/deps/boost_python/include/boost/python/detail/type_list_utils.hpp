#pragma once
#include <boost/python/detail/type_list.hpp>
#include <boost/python/cpp14/type_traits.hpp>

namespace boost { namespace python { namespace detail { namespace tl {

using detail::type_list;
struct invalid_type;

namespace impl {
    template<class List, std::size_t N, class...>
    struct sub;

    template<std::size_t N, class... Us>
    struct sub<type_list<>, N, Us...> {
        using type = type_list<Us...>;
    };

    template<class T, class... Tail, class... Us>
    struct sub<type_list<T, Tail...>, 0, Us...> {
        using type = type_list<Us...>;
    };

    template<std::size_t N, class T, class... Tail, class... Us>
    struct sub<type_list<T, Tail...>, N, Us...> {
        using type = typename sub<type_list<Tail...>, N - 1, Us..., T>::type;
    };
}

// Return the first N elements
template<class List, std::size_t N>
using sub_t = typename impl::sub<List, N>::type;

// Drop the last N elements from the list
template<class List, std::size_t N>
using drop_t = sub_t<List, List::is_empty ? 0 : List::size - N>;


namespace impl {
    template<class List1, class List2>
    struct concat;
    
    template<class... Ts, class... Us>
    struct concat<type_list<Ts...>, type_list<Us...>> {
        using type = type_list<Ts..., Us...>;
    };
}

// Concatenate two type_lists
template<class List1, class List2>
using concat_t = typename impl::concat<List1, List2>::type;


namespace impl {
    template<class List, std::size_t N>
    struct get {
        using type = invalid_type;
    };

    template<class T, class... Tail>
    struct get<type_list<T, Tail...>, 0> {
        using type = T;
    };

    template<std::size_t N, class T, class... Tail>
    struct get<type_list<T, Tail...>, N> {
        using type = typename get<type_list<Tail...>, N - 1>::type;
    };
}

// Get the Nth type, or invalid_type if the list is empty
template<class List, std::size_t N>
using get_t = typename impl::get<List, N>::type;

template<class List>
using front_t = get_t<List, 0>;

template<class List>
using back_t = get_t<List, List::is_empty ? 0 : List::size - 1>;

namespace impl {
    template<class List, template<class> class Predicate, class Default,
             class = void, bool = false>
    struct find_if;

    template<template<class> class Predicate, class Default, class U>
    struct find_if<type_list<>, Predicate, Default, U, false> {
        using type = Default;
    };

    template<template<class> class Predicate, class Default, class U, class... Ts>
    struct find_if<type_list<Ts...>, Predicate, Default, U, true> {
        using type = U;
    };

    template<template<class> class Predicate, class Default, class U, class T, class... Ts>
    struct find_if<type_list<T, Ts...>, Predicate, Default, U, false> {
        using type = typename find_if<
            type_list<Ts...>, Predicate, Default, T, Predicate<T>::value
        >::type;
    };
}

// Find the type that satisfies the Predicate or return Default if none do
template<class List, template<class> class Predicate, class Default = invalid_type>
using find_if_t = typename impl::find_if<List, Predicate, Default>::type;

namespace impl {
    template<bool...>
    struct bools {};

    template<class>
    struct always_false {
        static constexpr bool value = false;
    };

    template<class List, template<class> class Predicate>
    struct any_of;

    template<template<class> class Predicate, class... Ts>
    struct any_of<type_list<Ts...>, Predicate> {
        static constexpr bool value = !std::is_same<
            bools<Predicate<Ts>::value...>,
            bools<always_false<Ts>::value...>
        >::value;
    };
}

// Does any type satisfy the Predicate?
template<class List, template<class> class Predicate>
using any_of_t = std::integral_constant<bool, impl::any_of<List, Predicate>::value>;

}}}} // namespace boost::python::detail::tl
