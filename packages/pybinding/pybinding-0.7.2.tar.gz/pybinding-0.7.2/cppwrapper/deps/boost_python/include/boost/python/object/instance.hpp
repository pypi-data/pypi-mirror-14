// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef INSTANCE_DWA200295_HPP
# define INSTANCE_DWA200295_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/cpp14/type_traits.hpp>
# include <cstddef>

namespace boost { namespace python
{
  struct BOOST_PYTHON_DECL_FORWARD instance_holder;
}} // namespace boost::python

namespace boost { namespace python { namespace objects { 

// Each extension instance will be one of these
template <class Data = char>
struct instance
{
    PyObject_VAR_HEAD
    PyObject* dict;
    PyObject* weakrefs; 
    instance_holder* objects;

    cpp14::aligned_storage_t<sizeof(Data), alignof(Data)> storage;          
};

template <class Data>
struct additional_instance_size
{
    static constexpr auto value = 
        sizeof(instance<Data>) - offsetof(instance<char>, storage);
};

}}} // namespace boost::python::object

#endif // INSTANCE_DWA200295_HPP
