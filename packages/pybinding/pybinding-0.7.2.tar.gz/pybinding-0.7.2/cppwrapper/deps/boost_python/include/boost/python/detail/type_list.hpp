// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef TYPE_LIST_DWA2002913_HPP
# define TYPE_LIST_DWA2002913_HPP

namespace boost { namespace python { namespace detail { 

template<class... Ts>
struct type_list {
    static constexpr auto size = sizeof...(Ts);
    static constexpr bool is_empty = size == 0;
};
    
}}} // namespace boost::python::detail

#endif // TYPE_LIST_DWA2002913_HPP
