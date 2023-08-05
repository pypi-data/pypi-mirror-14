//  Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef REGISTRY_DWA20011127_HPP
# define REGISTRY_DWA20011127_HPP
# include <boost/python/type_id.hpp>
# include <boost/python/converter/registrations.hpp>

namespace boost { namespace python { namespace converter {

// This namespace acts as a sort of singleton
namespace registry
{
  // Get the registration corresponding to the type, creating it if necessary
  BOOST_PYTHON_DECL registration const& lookup(type_info, bool is_shared_ptr = false);

  // Return a pointer to the corresponding registration, if one exists
  BOOST_PYTHON_DECL registration const* query(type_info);

  BOOST_PYTHON_DECL void set_class_object(type_info, PyTypeObject*);
  BOOST_PYTHON_DECL void set_to_python_type(type_info cpptype, PyTypeObject const* pytype);

  BOOST_PYTHON_DECL void insert(to_python_function, type_info, pytype_function = nullptr);
  BOOST_PYTHON_DECL void insert_to_python_converter(to_python_function, type_info cpptype,
                                                    PyTypeObject const* pytype = nullptr);

  // Insert an lvalue from_python converter
  BOOST_PYTHON_DECL void insert(convertible_function, type_info, pytype_function = nullptr);
  BOOST_PYTHON_DECL void insert_lvalue_converter(convertible_function, type_info cpptype,
                                                 PyTypeObject const* pytype = nullptr);

  // Insert an rvalue from_python converter
  BOOST_PYTHON_DECL void insert(convertible_function, constructor_function, type_info,
                                pytype_function = nullptr);
  BOOST_PYTHON_DECL
  void insert_rvalue_converter(convertible_function, constructor_function, type_info cpptype,
                               PyTypeObject const* pytype = nullptr,
                               registration const* pytype_proxy = nullptr);

  // Insert an rvalue from_python converter at the tail of the
  // chain. Used for implicit conversions
  BOOST_PYTHON_DECL void push_back(convertible_function, constructor_function, type_info,
                                   pytype_function = nullptr);
  BOOST_PYTHON_DECL
  void insert_implicit_rvalue_converter(convertible_function, constructor_function,
                                        type_info cpptype, PyTypeObject const* pytype = nullptr,
                                        registration const* pytype_proxy = nullptr);

}

}}} // namespace boost::python::converter

#endif // REGISTRY_DWA20011127_HPP
