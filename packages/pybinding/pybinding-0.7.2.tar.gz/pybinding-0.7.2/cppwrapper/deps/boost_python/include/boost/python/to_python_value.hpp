// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef TO_PYTHON_VALUE_DWA200221_HPP
# define TO_PYTHON_VALUE_DWA200221_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/converter/registered.hpp>
# include <boost/python/converter/builtin_converters.hpp>
# include <boost/python/converter/object_manager.hpp>

namespace boost { namespace python { 

namespace detail
{
  template <class T>
  struct object_manager_to_python_value {
      PyObject* operator()(T const& x) const {
          return python::upcast<PyObject>(python::xincref(get_managed_object(x)));
      }
  };

  template <class T>
  struct registry_to_python_value {
      PyObject* operator()(T const& x) const {
          return converter::registered<T>::converters.to_python(&x);
      }

      // This information helps make_getter() decide whether to try to
      // return an internal reference or not. I don't like it much,
      // but it will have to serve for now.
      static constexpr bool uses_registry = true;
  };
}

// Assumes that T is a cv-unqualified non-reference type.
// Only instantiate this template using the 'make_to_python_value' alias.
template<class T>
struct to_python_value : cpp14::conditional_t<
    converter::is_object_manager<T>::value,
    detail::object_manager_to_python_value<T>,
    detail::registry_to_python_value<T>
> {};

template<class T>
using make_to_python_value = to_python_value<cpp14::remove_cv_t<cpp14::remove_reference_t<T>>>;

}} // namespace boost::python

#endif // TO_PYTHON_VALUE_DWA200221_HPP
