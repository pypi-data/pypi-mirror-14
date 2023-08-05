// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef BASES_DWA2002321_HPP
# define BASES_DWA2002321_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/detail/type_list.hpp>

namespace boost { namespace python { 

// A type list for specifying bases
template<class... Bases>
struct bases : detail::type_list<Bases...> {};

}} // namespace boost::python

#endif // BASES_DWA2002321_HPP
