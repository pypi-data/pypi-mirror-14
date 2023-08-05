// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/converter/from_python.hpp>
#include <boost/python/object/find_instance.hpp>
#include <boost/python/handle.hpp>

#include <vector>
#include <algorithm>

namespace boost { namespace python { namespace converter { 

// rvalue_from_python_stage1 -- do the first stage of a conversion
// from a Python object to a C++ rvalue.
//
//    source     - the Python object to be converted
//    converters - the registry entry for the target type T
//
// Postcondition: where x is the result, one of:
//
//   1. x.convertible == 0, indicating failure
//
//   2. x.construct == 0, x.convertible is the address of an object of
//      type T. Indicates a successful lvalue conversion
//
//   3. where y is of type rvalue_from_python_data<T>,
//      x.construct(source, y) constructs an object of type T
//      in y.storage.bytes and then sets y.convertible == y.storage.bytes,
//      or else throws an exception and has no effect.
BOOST_PYTHON_DECL
rvalue_from_python_stage1_data rvalue_from_python_stage1(PyObject* source,
                                                         registration const& converters)
{
    // First check to see if it's embedded in an extension class
    // instance, as a special case.
    auto embedded = objects::find_instance_impl(
        source, converters.target_type, converters.is_shared_ptr
    );
    if (embedded)
        return {embedded, nullptr};

    for (auto const& rvalue_converter : converters.rvalue_chain) {
        if (auto convertible = rvalue_converter.convertible(source))
            return {convertible, rvalue_converter.construct};
    }

    return {nullptr, nullptr};
}

BOOST_PYTHON_DECL
void* get_lvalue_from_python(PyObject* source, registration const& converters) {
    // Check to see if it's embedded in a class instance
    if (auto result = objects::find_instance_impl(source, converters.target_type))
        return result;

    for (auto& lvalue_converter : converters.lvalue_chain) {
        if (auto result = lvalue_converter.convert(source))
            return result;
    }

    return nullptr;
}

BOOST_PYTHON_DECL bool implicit_rvalue_convertible_from_python(PyObject* source,
                                                               registration const& converters)
{    
    if (objects::find_instance_impl(source, converters.target_type))
        return true;
    
    if (converters.is_being_visited)
        return false;
    converters.is_being_visited = true;

    auto is_convertible = std::any_of(
        converters.rvalue_chain.begin(), converters.rvalue_chain.end(),
        [source](registration::rvalue_from_python const& rvalue_converter) {
            return rvalue_converter.convertible(source);
        }
    );

    converters.is_being_visited = false;
    return is_convertible;
}

namespace errors {
    BOOST_PYTHON_DECL
    void throw_dangling_pointer(registration const& converters, char const* ref_type) {
        PyErr_Format(
            PyExc_ReferenceError,
            "Attempt to return dangling %s to object of type: %s",
            ref_type,
            converters.target_type.pretty_name().c_str()
        );
        throw_error_already_set();
    }

    BOOST_PYTHON_DECL
    void throw_bad_lvalue_conversion(PyObject* source, registration const& converters,
                                     char const* ref_type)
    {
        PyErr_Format(
            PyExc_TypeError,
            "No registered converter was able to extract a C++ %s to type %s"
            " from this Python object of type %s",
            ref_type,
            converters.target_type.pretty_name().c_str(),
            source->ob_type->tp_name
        );
        throw_error_already_set();
    }

    BOOST_PYTHON_DECL
    void throw_bad_rvalue_conversion(PyObject* source, registration const& converters) {
        PyErr_Format(
            PyExc_TypeError,
            "No registered converter was able to produce a C++ rvalue of type %s"
            " from this Python object of type %s",
            converters.target_type.pretty_name().c_str(),
            source->ob_type->tp_name
        );
        throw_error_already_set();
    }
} // namespace errors

} // namespace boost::python::converter

BOOST_PYTHON_DECL PyObject*
pytype_check(PyTypeObject* type_, PyObject* source)
{
    if (!PyObject_IsInstance(source, python::upcast<PyObject>(type_)))
    {
        ::PyErr_Format(
            PyExc_TypeError
            , "Expecting an object of type %s; got an object of type %s instead"
            , type_->tp_name
            , source->ob_type->tp_name
            );
        throw_error_already_set();
    }
    return source;
}

}} // namespace boost::python
