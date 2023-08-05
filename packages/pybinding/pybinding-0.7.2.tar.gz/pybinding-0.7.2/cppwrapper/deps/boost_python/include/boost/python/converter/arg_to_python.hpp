// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef ARG_TO_PYTHON_DWA200265_HPP
# define ARG_TO_PYTHON_DWA200265_HPP

# include <boost/python/ptr.hpp>
# include <boost/python/to_python_value.hpp>
# include <boost/python/to_python_indirect.hpp>
# include <boost/python/object/function_handle.hpp>
# include <boost/python/base_type_traits.hpp>

# ifdef BOOST_PYTHON_USE_STD_REF
#  include <functional>
# else
#  include <boost/ref.hpp>
# endif

namespace boost { namespace python { namespace converter {

# ifdef BOOST_PYTHON_USE_STD_REF
using std::reference_wrapper;
# else
using boost::reference_wrapper;
# endif

namespace detail
{
  template <class T>
  struct function_arg_to_python : handle<> {
      function_arg_to_python(T const& x)
          : handle<>(python::objects::make_function_handle(x))
      {}
  };

  template <class T>
  struct value_arg_to_python : handle<>  {
      value_arg_to_python(T const& x)
          : handle<>(to_python_value<T>{}(x))
      {}
  };

  template <class Ptr>
  struct pointer_deep_arg_to_python : handle<> {
      static_assert(!is_pyobject<cpp14::remove_pointer_t<Ptr>>::value,
                    "Passing a raw Python object pointer is not allowed");

      pointer_deep_arg_to_python(Ptr x)
          : handle<>(registered_pointee<Ptr>::converters.to_python(x))
      {}
  };

  template <class T>
  struct object_manager_arg_to_python {
      object_manager_arg_to_python(T const& x) : m_src(x) {}
      
      PyObject* get() const {
          return python::upcast<PyObject>(get_managed_object(m_src));
      }
      
  private:
      T const& m_src;
  };

  template <class T>
  using select_arg_to_python_t = cpp14::conditional_t<
      std::is_function<T>::value ||
      std::is_function<cpp14::remove_pointer_t<T>>::value ||
      std::is_member_function_pointer<T>::value,
      function_arg_to_python<T>,

      cpp14::conditional_t<
          is_object_manager<T>::value,
          object_manager_arg_to_python<T>,

          cpp14::conditional_t<
              std::is_pointer<T>::value,
              pointer_deep_arg_to_python<T>,
              value_arg_to_python<T>
          >
      >
  >;
}

// Throw an exception if the conversion can't succeed
template <class T>
struct arg_to_python : detail::select_arg_to_python_t<T> {
	arg_to_python(T const& x)
		: detail::select_arg_to_python_t<T>(x)
	{}
};

// Make sure char const* is not interpreted as a regular pointer
template<>
struct arg_to_python<char const*> : handle<> {
    arg_to_python(char const* x)
        : handle<>(to_python_value<char const*>{}(x))
    {}
};

// Interpret char[N] as char const* for the sake of conversion
template<std::size_t N>
struct arg_to_python<char[N]> : arg_to_python<char const*> {
    using arg_to_python<char const*>::arg_to_python;
};

// Shallow pointer to python
template<class Ptr>
struct arg_to_python<pointer_wrapper<Ptr>> : handle<> {
    static_assert(!is_pyobject<cpp14::remove_pointer_t<Ptr>>::value,
                  "Passing a raw Python object pointer is not allowed");

    arg_to_python(Ptr x)
        : handle<>(to_python_indirect<Ptr, python::detail::make_reference_holder>{}(x))
    {}
};

template<class T>
struct arg_to_python<reference_wrapper<T>> : handle<> {
    arg_to_python(T& x)
        : handle<>(to_python_indirect<T&, python::detail::make_reference_holder>{}(x))
    {}
};

}}} // namespace boost::python::converter

#endif // ARG_TO_PYTHON_DWA200265_HPP
