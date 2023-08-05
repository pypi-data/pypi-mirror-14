// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef OBJECT_CORE_DWA2002615_HPP
# define OBJECT_CORE_DWA2002615_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/handle.hpp>
# include <boost/python/errors.hpp>
# include <boost/python/refcount.hpp>
# include <boost/python/def_visitor.hpp>

# include <boost/python/object/add_to_namespace.hpp>

# include <boost/python/detail/raw_pyobject.hpp>
# include <boost/python/detail/string_literal.hpp>
# include <boost/python/detail/def_helper_fwd.hpp>
# include <boost/python/detail/none.hpp>

# include <boost/python/converter/to_python_fwd.hpp>

namespace boost { namespace python { 

namespace detail {
    struct args_proxy;
    struct kwargs_proxy;
}

// Put this in an inner namespace so that the generalized operators won't take over
namespace api
{
  
// This file contains the definition of the object class and enough to
// construct/copy it, but not enough to do operations like
// attribute/item access or addition.

  template <class Policies> class proxy;
  
  struct const_attribute_policies;
  struct attribute_policies;
  struct const_objattribute_policies;
  struct objattribute_policies;
  struct const_item_policies;
  struct item_policies;
  struct const_slice_policies;
  struct slice_policies;
  class slice_nil;

  typedef proxy<const_attribute_policies> const_object_attribute;
  typedef proxy<attribute_policies> object_attribute;
  typedef proxy<const_objattribute_policies> const_object_objattribute;
  typedef proxy<objattribute_policies> object_objattribute;
  typedef proxy<const_item_policies> const_object_item;
  typedef proxy<item_policies> object_item;
  typedef proxy<const_slice_policies> const_object_slice;
  typedef proxy<slice_policies> object_slice;

  class object;

  template <class U>
  class object_operators : public def_visitor<U> {
      using bool_type = PyObject* (object::*)() const;

  protected:
      using object_cref = object const&;

  public:
      // function call
      //
      template <typename... Args>
      object operator()(Args const&... args) const;

      detail::args_proxy operator*() const;
      object operator()(detail::args_proxy const& args) const;
      object operator()(detail::kwargs_proxy const& kwargs) const;
      object operator()(detail::args_proxy const& args,
                        detail::kwargs_proxy const& kwargs) const;

      // truth value testing
      //
      operator bool_type() const;

      // Attribute access
      //
      const_object_attribute attr(char const*) const;
      object_attribute attr(char const*);
      const_object_objattribute attr(object const&) const;
      object_objattribute attr(object const&);

      // Wrap 'in' operator (aka. __contains__)
      template <class T>
      object contains(T const& key) const;
      
      // item access
      //
      const_object_item operator[](object_cref) const;
      object_item operator[](object_cref);
    
      template <class T>
      const_object_item
      operator[](T const& key) const;
    
      template <class T>
      object_item
      operator[](T const& key);

      // slicing
      //
      const_object_slice slice(object_cref, object_cref) const;
      object_slice slice(object_cref, object_cref);

      const_object_slice slice(slice_nil, object_cref) const;
      object_slice slice(slice_nil, object_cref);
                             
      const_object_slice slice(object_cref, slice_nil) const;
      object_slice slice(object_cref, slice_nil);

      const_object_slice slice(slice_nil, slice_nil) const;
      object_slice slice(slice_nil, slice_nil);

      template <class T, class V>
      const_object_slice slice(T const& start, V const& end) const;
    
      template <class T, class V>
      object_slice slice(T const& start, V const& end);
      
  private: // def visitation for adding callable objects as class methods
      template <class ClassT, class DocStringT>
      void visit(ClassT& cl, char const* name,
                 python::detail::def_helper<DocStringT> const& helper) const
      {
          // It's too late to specify anything other than docstrings if
          // the callable object is already wrapped.
          static_assert(
              std::is_same<char const*, DocStringT>::value ||
              detail::is_string_literal<DocStringT const>::value, ""
          );
        
          objects::add_to_namespace(cl, name, this->derived_visitor(), helper.doc());
      }

      friend class python::def_visitor_access;

  private:
      U const& derived() const { return *static_cast<U const*>(this); }
      U& derived() { return *static_cast<U*>(this); }
  };

  class object : public object_operators<object> {
  public:
      // default constructor creates a None object
      object() noexcept : m_ptr{python::detail::none()} {}
      
      // explicit conversion from any C++ object to Python
      template<class T, class = cpp14::enable_if_t<!std::is_base_of<object, T>::value>>
      explicit object(T const& x)
          : m_ptr{incref(converter::arg_to_python<T>(x).get())}
      {}

      template<class T>
      explicit object(proxy<T> const& x)
          : m_ptr{incref(x.operator object().ptr())}
      {}

      // Throw error_already_set() if the handle is null.
      explicit object(handle<> const& x)
          : m_ptr{incref(expect_non_null(x.get()))}
      {}

      // copy constructor without NULL checking, for efficiency.
      object(object const& rhs) noexcept : m_ptr{incref(rhs.m_ptr)} {}
      object(object&& rhs) noexcept : m_ptr{rhs.release()} {}

      object& operator=(object const& rhs) noexcept {
          incref(rhs.m_ptr);
          decref(m_ptr);
          m_ptr = rhs.m_ptr;
          return *this;
      }

      object& operator=(object&& rhs) noexcept {
          decref(m_ptr);
          m_ptr = rhs.release();
          return *this;
      }

      ~object() { decref(m_ptr); }

      // Underlying object access -- returns a borrowed reference
      PyObject* ptr() const noexcept { return m_ptr; }
      // Underlying object access -- returns an owned reference
      PyObject* release() noexcept {
          auto result = m_ptr;
          m_ptr = python::detail::none();
          return result;
      }

      bool is_none() const noexcept { return m_ptr == Py_None; }

  private:
      PyObject* m_ptr;

  public: // implementation detail -- for internal use only
      explicit object(detail::borrowed_reference p) noexcept : m_ptr{incref((PyObject*)p)} {}
      explicit object(detail::new_reference p) : m_ptr{expect_non_null((PyObject*)p)} {}
      explicit object(detail::new_non_null_reference p) noexcept : m_ptr{(PyObject*)p} {}
  };

  // Macros for forwarding constructors in classes derived from
  // object. Derived classes will usually want these as an
  // implementation detail
# define BOOST_PYTHON_FORWARD_OBJECT_CONSTRUCTORS(derived, base)                        \
    inline explicit derived(::boost::python::detail::borrowed_reference p) noexcept     \
        : base(p) {}                                                                    \
    inline explicit derived(::boost::python::detail::new_reference p)                   \
        : base(p) {}                                                                    \
    inline explicit derived(::boost::python::detail::new_non_null_reference p) noexcept \
        : base(p) {}

} // namespace api
using api::object;

//
// implementation
//

template <typename U>
template <class T>
object api::object_operators<U>::contains(T const& key) const {
    return this->attr("__contains__")(object(key));
}


//
// Converter specialization implementations
//
namespace converter
{
  template <class T> struct object_manager_traits;
  
  template <>
  struct object_manager_traits<object> {
      static constexpr bool is_specialized = true;
      static bool check(PyObject*) { return true; }
      
      static python::detail::new_non_null_reference adopt(PyObject* x) {
          return python::detail::new_non_null_reference(x);
      }
  };
}

inline PyObject* get_managed_object(object const& x) {
    return x.ptr();
}

}} // namespace boost::python

#endif // OBJECT_CORE_DWA2002615_HPP
