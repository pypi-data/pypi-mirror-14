// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef DEF_HELPER_DWA200287_HPP
# define DEF_HELPER_DWA200287_HPP

# include <boost/python/args.hpp>
# include <boost/python/detail/def_helper_fwd.hpp>

# include <boost/python/cpp14/type_traits.hpp>
# include <tuple>

namespace boost { namespace python {
    struct default_call_policies;
}}

namespace boost { namespace python { namespace detail {

template<template<class> class Predicate, class Tuple>
struct tuple_find_if;

template<template<class> class Predicate, class... Args>
struct tuple_find_if<Predicate, std::tuple<Args...>> {
    // Predicate result is 'true', return the index
    template<bool result, int index, class...>
    struct find_index {
        static constexpr auto value = index;
    };

    // Predicate result is 'false', test the next element
    template<int index, class T, class... Tail>
    struct find_index<false, index, T, Tail...> {
        using U = cpp14::remove_cv_t<cpp14::remove_reference_t<T>>;
        static constexpr auto value = find_index<Predicate<U>::value, index + 1, Tail...>::value;
    };

    // Not found
    template<int index>
    struct find_index<false, index> {
        static constexpr auto value = -1;
    };

    static constexpr auto value = find_index<false, -1, Args...>::value;
};

template<std::size_t index, class Else, class Tuple>
auto get_if_else_impl(Tuple const& t, std::true_type) -> decltype(std::get<index>(t)) {
    return std::get<index>(t);
}

template<std::size_t index, class Else, class Tuple>
Else get_if_else_impl(Tuple const&, std::false_type) {
    return {};
}

// Get the first tuple element that satisfies the Predicate template.
// If no element is found, return a default constructed value of Else.
// References and cv qualifiers are removed from the element type
// before passing it to the predicate.
template<template<class> class Predicate, class Else, class Tuple,
    int index_ = tuple_find_if<Predicate, Tuple>::value, 
	bool found = (index_ >= 0), std::size_t index = found ? index_ : 0>
auto get_if_else(Tuple const& t)
    -> decltype(get_if_else_impl<index, Else>(t, std::integral_constant<bool, found>{}))
{
    return get_if_else_impl<index, Else>(t, std::integral_constant<bool, found>{});
}

// A helper class for decoding the optional arguments to def()
// invocations, which can be supplied in any order and are
// discriminated by their type properties. The template parameters
// are expected to be the types of the actual (optional) arguments
// passed to def().
template<class... Args>
struct def_helper {
    def_helper(Args const&... args) : args{args...} {}

private:
    using tuple = std::tuple<Args const&...>;

    // A function pointer type which is never an appropriate default implementation
    using invalid_default = void (def_helper::*)();

    template<class T>
    struct is_doc {
        static constexpr bool value = !std::is_class<T>::value &&
                                      !std::is_member_function_pointer<T>::value;
    };

    template<class T>
    struct is_policy {
        static constexpr bool value = std::is_class<T>::value && !is_keywords<T>::value;
    };

public: // Constants which can be used for static assertions.
    // Users must not supply a default implementation for non-class methods.
    static constexpr bool has_default_implementation =
        tuple_find_if<std::is_member_function_pointer, tuple>::value >= 0;

public: // Extractor functions which pull the appropriate value out of the tuple
    char const* doc() const {
        return get_if_else<is_doc, char const*>(args);
    }

    auto keywords() const -> decltype(get_if_else<is_keywords, detail::keywords<>>(std::declval<tuple>())) {
        return get_if_else<is_keywords, detail::keywords<>>(args);
    }

    auto policies() const -> decltype(get_if_else<is_policy, default_call_policies>(std::declval<tuple>())) {
        return get_if_else<is_policy, default_call_policies>(args);
    }

    auto default_implementation() const -> decltype(get_if_else<std::is_member_function_pointer, invalid_default>(std::declval<tuple>())) {
        return get_if_else<std::is_member_function_pointer, invalid_default>(args);
    }

private:
    tuple args;
};

template<class... Args>
def_helper<Args...> make_def_helper(Args const&... args) {
    return {args...};
}

}}} // namespace boost::python::detail

#endif // DEF_HELPER_DWA200287_HPP
