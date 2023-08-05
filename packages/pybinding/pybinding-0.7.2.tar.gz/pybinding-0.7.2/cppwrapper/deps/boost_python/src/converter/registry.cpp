//  Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#include <boost/python/converter/registry.hpp>
#include <boost/python/converter/builtin_converters.hpp>

#include <set>

#if defined(BOOST_PYTHON_TRACE_REGISTRY)
# include <iostream>
#endif

namespace boost { namespace python { namespace converter {

BOOST_PYTHON_DECL PyTypeObject const* registration::expected_from_python_type() const
{
    if (m_class_object)
        return m_class_object;

    std::set<PyTypeObject const*> pool;
    for (auto const& rvalue_converter : rvalue_chain) {
        if (rvalue_converter.pytype) {
            pool.insert(rvalue_converter.pytype);
        }
        else if (rvalue_converter.pytype_proxy) {
            // A type proxy is used with converters like shared_ptr<T>
            // where we're actually interested in the python type of T.
            if (auto pytype = rvalue_converter.pytype_proxy->expected_from_python_type())
                pool.insert(pytype);
        }
    }

    //for now I skip the search for common base
    if (pool.size()==1)
        return *pool.begin();

    return nullptr;
}

BOOST_PYTHON_DECL PyTypeObject const* registration::to_python_target_type() const
{
    if (m_class_object)
        return m_class_object;

    if (to_python_pytype)
        return to_python_pytype;

    return nullptr;
}

BOOST_PYTHON_DECL PyTypeObject* registration::get_class_object() const
{
    if (!m_class_object) {
        PyErr_Format(PyExc_TypeError, "No Python class registered for C++ class %s",
                     target_type.pretty_name().c_str());
        throw_error_already_set();
    }
    
    return m_class_object;
}
  
BOOST_PYTHON_DECL PyObject* registration::to_python(void const* source) const
{
    if (!m_to_python) {
        PyErr_Format(PyExc_TypeError, "No to_python (by-value) converter found for C++ type: %s",
                     target_type.pretty_name().c_str());
        throw_error_already_set();
    }

    return (source == nullptr) ? python::detail::none() : m_to_python(source);
}


namespace // <unnamed>
{
  using registry_t = std::set<registration>;
  
  registry_t& entries()
  {
      static registry_t registry;

# ifndef BOOST_PYTHON_SUPPRESS_REGISTRY_INITIALIZATION
      static bool builtin_converters_initialized = false;
      if (!builtin_converters_initialized)
      {
          // Make this true early because registering the builtin
          // converters will cause recursion.
          builtin_converters_initialized = true;
          
          initialize_builtin_converters();
      }
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      std::cout << "registry: ";
      for (auto const& p : registry) {
          std::cout << p->target_type << "; ";
      }
      std::cout << '\n';
#  endif 
# endif 
      return registry;
  }

  registration& get_registration(type_info cpptype, bool is_shared_ptr = false)
  {
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      auto p = entries().find(registration(cpptype));
      std::cout << "looking up " << cpptype << ": "
                << (p == entries().end() || p->target_type != cpptype
                    ? "...NOT found\n" : "...found\n");
#  endif
      auto pos_ins = entries().emplace(cpptype, is_shared_ptr);
      return const_cast<registration&>(*pos_ins.first);
  }
} // namespace <unnamed>

namespace registry
{
  void insert(to_python_function to_python, type_info cpptype, pytype_function target_pytype) {
      insert_to_python_converter(to_python, cpptype, target_pytype ? target_pytype() : nullptr);
  }

  void insert_to_python_converter(to_python_function to_python, type_info cpptype,
                                  PyTypeObject const* pytype)
  {
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      std::cout << "inserting to_python " << cpptype << "\n";
#  endif 
      auto& slot = get_registration(cpptype);
      
      assert(slot.m_to_python == nullptr); // we have a problem otherwise
      if (slot.m_to_python) {
          auto msg = std::string("to-Python converter for ") + cpptype.pretty_name()
              + " already registered; second conversion method ignored.";
          
          if (PyErr_WarnEx(nullptr, msg.c_str(), 1))
              throw_error_already_set();
      }

      slot.m_to_python = to_python;
      slot.to_python_pytype = pytype;
  }

  // Insert an lvalue from_python converter
  void insert(convertible_function convertible, type_info cpptype, pytype_function exp_pytype) {
      insert_lvalue_converter(convertible, cpptype, exp_pytype ? exp_pytype() : nullptr);
  }

  void insert_lvalue_converter(convertible_function convertible, type_info cpptype,
                               PyTypeObject const* pytype)
  {
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      std::cout << "inserting lvalue from_python " << cpptype << "\n";
#  endif 
      auto& slot = get_registration(cpptype);
      slot.lvalue_chain.push_front({convertible});

      insert_rvalue_converter(convertible, nullptr, cpptype, pytype);
  }

  // Insert an rvalue from_python converter
  void insert(convertible_function convertible, constructor_function construct,
              type_info cpptype, pytype_function exp_pytype)
  {
      insert_rvalue_converter(convertible, construct, cpptype, exp_pytype ? exp_pytype() : nullptr);
  }

  void insert_rvalue_converter(convertible_function convertible, constructor_function construct,
                               type_info cpptype, PyTypeObject const* pytype,
                               registration const* proxy)
  {
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      std::cout << "inserting rvalue from_python " << cpptype << "\n";
#  endif 
      auto& slot = get_registration(cpptype);
      slot.rvalue_chain.push_front({convertible, construct, pytype, proxy});
  }

  // Insert an rvalue from_python converter
  void push_back(convertible_function convertible, constructor_function construct,
                 type_info cpptype, pytype_function exp_pytype)
  {
      insert_implicit_rvalue_converter(convertible, construct, cpptype,
                                       exp_pytype ? exp_pytype() : nullptr);
  }

  void insert_implicit_rvalue_converter(
      convertible_function convertible, constructor_function construct,
      type_info cpptype, PyTypeObject const* pytype, registration const* proxy
  ) {
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      std::cout << "push_back rvalue from_python " << cpptype << "\n";
#  endif 
      auto& slot = get_registration(cpptype);

      auto before_end = slot.rvalue_chain.before_begin();
      while (std::next(before_end) != slot.rvalue_chain.end())
          ++before_end;

      slot.rvalue_chain.insert_after(before_end, {convertible, construct, pytype, proxy});
  }

  registration const& lookup(type_info cpptype, bool is_shared_ptr)
  {
      return get_registration(cpptype, is_shared_ptr);
  }

  registration const* query(type_info cpptype)
  {
      auto p = entries().find(registration(cpptype));
#  ifdef BOOST_PYTHON_TRACE_REGISTRY
      std::cout << "querying " << cpptype
                << (p == entries().end() || p->target_type != cpptype
                    ? "...NOT found\n" : "...found\n");
#  endif 
      return (p == entries().end() || p->target_type != cpptype) ? nullptr : &*p;
  }

  void set_class_object(type_info cpptype, PyTypeObject* class_object)
  {
      auto& slot = get_registration(cpptype);
      slot.m_class_object = class_object;
  }

  void set_to_python_type(type_info cpptype, PyTypeObject const* pytype) {
      if (!pytype)
          return;

      auto& slot = get_registration(cpptype);
      if (!slot.to_python_pytype)
          slot.to_python_pytype = pytype;
  }

} // namespace registry

}}} // namespace boost::python::converter
