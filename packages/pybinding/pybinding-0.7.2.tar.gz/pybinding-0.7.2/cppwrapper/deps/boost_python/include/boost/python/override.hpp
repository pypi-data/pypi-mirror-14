// Copyright David Abrahams 2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#ifndef OVERRIDE_DWA2004721_HPP
# define OVERRIDE_DWA2004721_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/converter/return_from_python.hpp>

# include <boost/python/extract.hpp>
# include <boost/python/handle.hpp>

namespace boost { namespace python {

class override;

namespace detail
{
  // The result of calling a method.
  class method_result {
  private:
      friend class boost::python::override;
      explicit method_result(PyObject* x) : m_obj{x} {}

  public:
      template <class T>
      operator T() {
          return converter::return_from_python<T>{}(m_obj.release());
      };
      
#  ifdef _MSC_VER
	  template <class T>
	  operator T*() {
		  return converter::return_from_python<T*>{}(m_obj.release());
	  }
#  endif 

#  if _MSC_VER
	  // No operator T&
#  else
      template <class T>
      operator T&() const {
          return converter::return_from_python<T&>{}(m_obj.release());
      };
#endif

      template <class T>
      T as() {
          return converter::return_from_python<T>{}(m_obj.release());
      };

      template <class T>
      T unchecked() {
          return extract<T>{m_obj.get()}();
      };

  private:
      mutable handle<> m_obj;
  };
}

class override : public object {
private:
    friend class detail::wrapper_base;
    override(handle<> x) : object{x} {}
    
public:
    template<class... Args>
    detail::method_result operator()(Args const&... args) const {
        return detail::method_result{
            PyObject_CallFunctionObjArgs(
                ptr(), converter::arg_to_python<Args>(args).get()..., nullptr
            )
        };
    }
};

}} // namespace boost::python

#endif // OVERRIDE_DWA2004721_HPP
