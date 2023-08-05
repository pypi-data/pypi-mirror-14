// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef HANDLE_DWA200269_HPP
# define HANDLE_DWA200269_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/cast.hpp>
# include <boost/python/errors.hpp>
# include <boost/python/borrowed.hpp>
# include <boost/python/handle_fwd.hpp>
# include <boost/python/refcount.hpp>
# include <boost/python/detail/raw_pyobject.hpp>

namespace boost { namespace python { 

template <class T> struct null_ok;

template<class T = PyObject>
inline null_ok<T>* allow_null(T* p = nullptr) noexcept {
    return (null_ok<T>*)p;
}

namespace detail
{
  template <class T>
  inline T* manage_ptr(detail::borrowed<null_ok<T> >* p) noexcept {
      return python::xincref((T*)p);
  }
  
  template <class T>
  inline T* manage_ptr(null_ok<detail::borrowed<T> >* p) noexcept {
      return python::xincref((T*)p);
  }
  
  template <class T>
  inline T* manage_ptr(detail::borrowed<T>* p) {
      return python::incref(expect_non_null((T*)p));
  }
  
  template <class T>
  inline T* manage_ptr(null_ok<T>* p) noexcept {
      return (T*)p;
  }
  
  template <class T>
  inline T* manage_ptr(T* p) {
      return expect_non_null(p);
  }
}

template <class T>
class handle {
public: // types
    using element_type = T;

public: // member functions
    handle() = default;
    ~handle() { xdecref(m_p); }

    template <class Y>
    explicit handle(Y* p) : m_p{upcast<T>(detail::manage_ptr(p))} {}

    handle(handle const& r) noexcept : m_p{xincref(r.m_p)} {}

    template <typename Y>
    handle(handle<Y> const& r) noexcept : m_p{xincref(upcast<T>(r.get()))} {}

    handle& operator=(handle const& r) noexcept {
        xdecref(m_p);
        m_p = xincref(r.m_p);
        return *this;
    }

    template<typename Y>
    handle& operator=(handle<Y> const& r) noexcept {
        xdecref(m_p);
        m_p = xincref(upcast<T>(r.get()));
        return *this;
    }

    handle(handle&& r) noexcept : m_p{r.release()} {}

    template <typename Y>
    handle(handle<Y>&& r) noexcept : m_p{upcast<T>(r.release())} {}

    handle& operator=(handle&& r) noexcept {
        xdecref(m_p);
        m_p = r.release();
        return *this;
    }

    template<typename Y>
    handle& operator=(handle<Y>&& r) noexcept {
        xdecref(m_p);
        m_p = upcast<T>(r.release());
        return *this;
    }

    T* operator->() const noexcept { return m_p; }
    T& operator*() const noexcept { return *m_p; }
    T* get() const noexcept { return m_p; }

    T* release() noexcept {
        auto result = m_p;
        m_p = nullptr;
        return result;
    }
    void reset() noexcept {
        python::xdecref(m_p);
        m_p = nullptr;
    }
    
    explicit operator bool() const noexcept { return m_p != nullptr; }

public: // implementation details -- do not touch
    handle(detail::borrowed_reference x) noexcept : m_p{incref(downcast<T>((PyObject*)x))} {}
    
 private: // data members
    T* m_p = nullptr;
};

using type_handle = handle<PyTypeObject>;

// Compile-time introspection
template<typename T>
struct is_handle : std::false_type {};

template<typename T>
struct is_handle<handle<T>> : std::true_type {};

// Because get_managed_object must return a non-null PyObject*, we
// return Py_None if the handle is null.
template <class T>
inline PyObject* get_managed_object(handle<T> const& h) noexcept {
    return h.get() ? python::upcast<PyObject>(h.get()) : Py_None;
}

}} // namespace boost::python

#endif // HANDLE_DWA200269_HPP
