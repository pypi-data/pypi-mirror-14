// Copyright David Abrahams 2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#ifndef VALUE_ARG_DWA2004312_HPP
# define VALUE_ARG_DWA2004312_HPP

# include <boost/python/detail/copy_ctor_mutates_rhs.hpp>
# include <boost/python/cpp14/type_traits.hpp>

namespace boost { namespace python { namespace detail { 

template <class T>
using value_arg_t = cpp14::conditional_t<
    copy_ctor_mutates_rhs<T>::value,
    T,
    cpp14::add_lvalue_reference_t<cpp14::add_const_t<T>>
>;
  
}}} // namespace boost::python::detail

#endif // VALUE_ARG_DWA2004312_HPP
