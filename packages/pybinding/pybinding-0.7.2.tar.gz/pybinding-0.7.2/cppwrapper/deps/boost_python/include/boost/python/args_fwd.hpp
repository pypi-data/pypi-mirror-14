// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef ARGS_FWD_DWA2002927_HPP
# define ARGS_FWD_DWA2002927_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/handle.hpp>

namespace boost { namespace python { 

namespace detail
{
  struct keyword {
      keyword(char const* name = nullptr) : name(name) {}
      
      char const* name;
      handle<> default_value;
  };
  
  template <std::size_t nkeywords = 0> struct keywords;
  
  using keyword_range = std::pair<keyword const*, keyword const*>;
  
  template <>
  struct keywords<0> {
      static constexpr auto size = 0;
      static keyword_range range() { return {}; }
  };
}

}} // namespace boost::python

#endif // ARGS_FWD_DWA2002927_HPP
