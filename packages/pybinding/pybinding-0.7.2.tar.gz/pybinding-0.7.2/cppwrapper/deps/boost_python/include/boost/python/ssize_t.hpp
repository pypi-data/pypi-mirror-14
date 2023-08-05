// Copyright Ralf W. Grosse-Kunstleve & David Abrahams 2006.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef BOOST_PYTHON_SSIZE_T_RWGK20060924_HPP
# define BOOST_PYTHON_SSIZE_T_RWGK20060924_HPP

# include <boost/python/detail/prefix.hpp>

namespace boost { namespace python {

using ssize_t = Py_ssize_t;
constexpr ssize_t ssize_t_max = PY_SSIZE_T_MAX;
constexpr ssize_t ssize_t_min = PY_SSIZE_T_MIN;

}} // namespace boost::python

#endif // BOOST_PYTHON_SSIZE_T_RWGK20060924_HPP
