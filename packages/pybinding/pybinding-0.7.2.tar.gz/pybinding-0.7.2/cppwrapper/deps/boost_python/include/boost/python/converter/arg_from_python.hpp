// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef ARG_FROM_PYTHON_DWA2002127_HPP
# define ARG_FROM_PYTHON_DWA2002127_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/converter/from_python.hpp>
# include <boost/python/converter/registry.hpp>
# include <boost/python/converter/registered.hpp>
# include <boost/python/back_reference.hpp>
# include <boost/python/converter/object_manager.hpp>
# include <boost/python/detail/raw_pyobject.hpp>
# include <boost/python/cpp14/type_traits.hpp>

// This header defines Python->C++ function argument converters,
// parametrized on the argument type.

namespace boost { namespace python { namespace converter {

template <class T> struct arg_from_python;

// Converter for Python type wrappers.
template<class T>
struct object_manager_arg_from_python {
    using object_manager = cpp14::remove_cv_t<cpp14::remove_reference_t<T>>;

    object_manager_arg_from_python(PyObject* source)
        : result{python::detail::borrowed_reference(source)}
    {}

    bool check() const {
        return object_manager_traits<object_manager>::check(get_managed_object(result));
    }

    T&& operator()() { return static_cast<T&&>(result); }

private:
    object_manager result;
};

// Converts to a (PyObject*,T) bundle, for when you need a reference
// back to the Python object
template <class T>
struct back_reference_arg_from_python : arg_from_python<typename T::type> {
private:
    using base = arg_from_python<typename T::type>;
    PyObject* m_source;

public:
    back_reference_arg_from_python(PyObject* p) : base(p), m_source(p) {}
    T operator()() { return T(m_source, base::operator()()); }
};


// This metafunction selects the appropriate arg_from_python converter
// type for an argument of type T.
template<class T, class T_without_ref = cpp14::remove_reference_t<T>,
         class T_without_ref_and_cv = cpp14::remove_cv_t<T_without_ref>>
using select_arg_from_python_t = cpp14::conditional_t<
    is_object_manager<T_without_ref_and_cv>::value,
    object_manager_arg_from_python<T>,

    cpp14::conditional_t< // T == U* or T == U*const&
        std::is_pointer<T>::value ||
        (std::is_reference<T>::value &&
         std::is_pointer<T_without_ref>::value &&
         std::is_const<T_without_ref>::value &&
         !std::is_volatile<T_without_ref>::value),
        lvalue_from_python<T_without_ref_and_cv>,

        cpp14::conditional_t< // T == U& and (T != V const& or T == W volatile&)
            std::is_reference<T>::value &&
            (!std::is_const<T_without_ref>::value || std::is_volatile<T_without_ref>::value),
            lvalue_from_python<T>,

            cpp14::conditional_t<
                boost::python::is_back_reference<T>::value,
                back_reference_arg_from_python<T>,

                rvalue_from_python<T> // T is a plain value U or U const&
            >
        >
    >
>;

template <class T>
struct arg_from_python : select_arg_from_python_t<T> {
    using select_arg_from_python_t<T>::select_arg_from_python_t;
};

// specialization for PyObject*
template <>
struct arg_from_python<PyObject*> {
    using result_type = PyObject*;

    arg_from_python(PyObject* p) : m_source(p) {}
    bool check() const { return true; }
    result_type operator()() const { return m_source; }

private:
    PyObject* m_source;
};

template <>
struct arg_from_python<PyObject* const&> {
    using result_type = PyObject* const&;

    arg_from_python(PyObject* p) : m_source(p) {}
    bool check() const { return true; }
    result_type operator()() const { return m_source; }

private:
    PyObject* m_source;
};

}}} // namespace boost::python::converter

#endif // ARG_FROM_PYTHON_DWA2002127_HPP
