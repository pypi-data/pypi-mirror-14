// Copyright David Abrahams 2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#ifndef UNWRAP_WRAPPER_DWA2004723_HPP
# define UNWRAP_WRAPPER_DWA2004723_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/detail/void_t.hpp>

namespace boost { namespace python { namespace detail { 

template<class T, class = void>
struct unwrap_wrapper {
    using type = T;
};

template<class T>
struct unwrap_wrapper<T, void_t<typename T::_wrapper_wrapped_type_>> {
    using type = typename T::_wrapper_wrapped_type_;
};

template<class T>
using unwrap_wrapper_t = typename unwrap_wrapper<T>::type;

}}} // namespace boost::python::detail

#endif // UNWRAP_WRAPPER_DWA2004723_HPP
