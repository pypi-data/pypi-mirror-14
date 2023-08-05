// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef STRING_LITERAL_DWA2002629_HPP
# define STRING_LITERAL_DWA2002629_HPP

# include <type_traits>

namespace boost { namespace python { namespace detail { 

template <class T>
struct is_string_literal : std::false_type {};

template <std::size_t n>
struct is_string_literal<char const[n]> : std::true_type {};

}}} // namespace boost::python::detail

#endif // STRING_LITERAL_DWA2002629_HPP
