// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef OVERLOADS_FWD_DWA2002101_HPP
# define OVERLOADS_FWD_DWA2002101_HPP

namespace boost { namespace python { namespace detail { 

// forward declarations
struct overloads_base;
  
template<class Signature, class Overloads, class Namespace>
inline void define_with_defaults(char const* name, Overloads const&, Namespace&);

}}} // namespace boost::python::detail

#endif // OVERLOADS_FWD_DWA2002101_HPP
