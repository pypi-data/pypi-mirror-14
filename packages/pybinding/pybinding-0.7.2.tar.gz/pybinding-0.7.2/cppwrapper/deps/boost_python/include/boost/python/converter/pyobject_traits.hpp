// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef PYOBJECT_TRAITS_DWA2002720_HPP
# define PYOBJECT_TRAITS_DWA2002720_HPP

# include <boost/python/detail/prefix.hpp>

namespace boost { namespace python { namespace converter { 

template <class> struct pyobject_traits;

template <>
struct pyobject_traits<PyObject> {
    // All objects are convertible to PyObject
    static bool check(PyObject*) { return true; }
    static PyObject* checked_downcast(PyObject* x) { return x; }
};

//
// Specializations
//
template<class Object, PyTypeObject* pytype>
struct pyobject_traits_specialization {
    static bool check(PyObject* x) {
        return PyObject_IsInstance(x, (PyObject*)pytype);
    }

    static Object* checked_downcast(PyObject* p) {
        return python::downcast<Object>(python::pytype_check(pytype, p));
    }

};

# define BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(T)                     \
template<>                                                         \
struct pyobject_traits<Py##T##Object>                              \
    : pyobject_traits_specialization<Py##T##Object, &Py##T##_Type> \
{};

// This is not an exhaustive list; should be expanded.
BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(Type);
BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(List);
#if PY_VERSION_HEX < 0x03000000
BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(Int);
#endif
BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(Long);
BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(Dict);
BOOST_PYTHON_BUILTIN_OBJECT_TRAITS(Tuple);

}}} // namespace boost::python::converter

#endif // PYOBJECT_TRAITS_DWA2002720_HPP
