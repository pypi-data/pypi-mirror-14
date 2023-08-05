// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef REGISTRATIONS_DWA2002223_HPP
# define REGISTRATIONS_DWA2002223_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/type_id.hpp>
# include <forward_list>

namespace boost { namespace python { namespace converter {

// The type of stored function pointers which actually do conversion
// by-value. The void* points to the object to be converted, and
// type-safety is preserved through runtime registration.
using to_python_function = PyObject* (*)(void const*);

using pytype_function = PyTypeObject const* (*)();
using convertible_function = void* (*)(PyObject*);

// Declares the type of functions used to construct C++ objects for
// rvalue from_python conversions.
struct rvalue_from_python_stage1_data;
using constructor_function = void (*)(PyObject* source, rvalue_from_python_stage1_data*);

struct BOOST_PYTHON_DECL registration {
    struct lvalue_from_python {
        convertible_function convert;
    };

    struct rvalue_from_python {
        convertible_function convertible;
        constructor_function construct;
        PyTypeObject const* pytype;
        registration const* pytype_proxy;
    };

public: // member functions
    explicit registration(type_info target, bool is_shared_ptr = false)
        : target_type(target), is_shared_ptr(is_shared_ptr) {}

    // Check that a to_python converter exists
    bool has_to_python() const { return m_to_python != nullptr; }
    // Convert the appropriately-typed data to Python
    PyObject* to_python(void const*) const;

    // Return the class object, or raise an appropriate Python
    // exception if no class has been registered.
    PyTypeObject* get_class_object() const;

    // Return common denominator of the python class objects, 
    // convertable to target. Inspects the m_class_object and the value_chains.
    PyTypeObject const* expected_from_python_type() const;
    PyTypeObject const* to_python_target_type() const;

public: // data members. So sue me.
    const python::type_info target_type;

    // The chain of eligible from_python converters when an lvalue is required
    std::forward_list<lvalue_from_python> lvalue_chain;

    // The chain of eligible from_python converters when an rvalue is acceptable
    std::forward_list<rvalue_from_python> rvalue_chain;

    // The class object associated with this type
    PyTypeObject* m_class_object = nullptr;

    // The unique to_python converter for the associated C++ type.
    to_python_function m_to_python = nullptr;
    PyTypeObject const* to_python_pytype = nullptr;

    // True iff this type is a shared_ptr.  Needed for special rvalue
    // from_python handling.
    const bool is_shared_ptr;

public:
    // Prevent looping in implicit conversions.
    mutable bool is_being_visited = false;
};

inline bool operator<(registration const& lhs, registration const& rhs)
{
    return lhs.target_type < rhs.target_type;
}

}}} // namespace boost::python::converter

#endif // REGISTRATIONS_DWA2002223_HPP
