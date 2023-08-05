#ifndef OTHER_DWA20020601_HPP
# define OTHER_DWA20020601_HPP

# include <boost/python/detail/prefix.hpp>
// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

namespace boost { namespace python {

template<class T> struct other {
    using type = T;
};

namespace detail
{
  template<typename T>
  struct is_other {
      static constexpr bool value = false;
  };

  template<typename T>
  struct is_other<other<T>> {
      static constexpr bool value = true;
  };

  template<typename T>
  struct unwrap_other {
      using type = T;
  };

  template<typename T>
  struct unwrap_other<other<T>> {
      using type = T;
  };
}

}} // namespace boost::python

#endif // #ifndef OTHER_DWA20020601_HPP
