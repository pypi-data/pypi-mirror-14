// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef CAST_DWA200269_HPP
# define CAST_DWA200269_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/base_type_traits.hpp>

namespace boost { namespace python { 

namespace detail {
  // PyObject C structs must use C casts, while everything else should use C++ casts.
  template <class Target, class Source>
  inline Target* upcast(Source* p, std::false_type) { return p; }
    
  template <class Target, class Source>
  inline Target* upcast(Source* p, std::true_type) { return (Target*)p; }

  template <class Target, class Source>
  inline Target* downcast(Source* p, std::false_type) { return static_cast<Target*>(p); }

  template <class Target, class Source>
  inline Target* downcast(Source* p, std::true_type) { return (Target*)p; }
}

template <class Target, class Source>
inline Target* upcast(Source* p) {
    return detail::upcast<Target>(p, is_c_pyobject<Source>{});
}

template <class Target, class Source>
inline Target* downcast(Source* p) {
    return detail::downcast<Target>(p, is_c_pyobject<Source>{});
}

}} // namespace boost::python

#endif // CAST_DWA200269_HPP
