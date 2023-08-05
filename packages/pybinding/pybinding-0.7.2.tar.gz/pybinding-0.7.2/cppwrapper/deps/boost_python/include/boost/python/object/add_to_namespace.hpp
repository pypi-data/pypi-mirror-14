// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef ADD_TO_NAMESPACE_DWA200286_HPP
# define ADD_TO_NAMESPACE_DWA200286_HPP

# include <boost/python/object_fwd.hpp>

namespace boost { namespace python { namespace objects { 

// Add an attribute to the name_space with the given name. If it is
// a Boost.Python function object (boost/python/object/function.hpp)
// and an existing function is already there, add it as an overload.
BOOST_PYTHON_DECL void add_to_namespace(object const& name_space, char const* name,
                                        object const& attribute, char const* doc = nullptr);

}}} // namespace boost::python::objects

#endif // ADD_TO_NAMESPACE_DWA200286_HPP
