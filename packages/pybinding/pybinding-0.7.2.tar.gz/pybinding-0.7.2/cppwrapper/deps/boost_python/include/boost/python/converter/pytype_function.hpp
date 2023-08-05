// Copyright David Abrahams 2002,  Nikolay Mladenov 2007.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef WRAP_PYTYPE_NM20070606_HPP
# define WRAP_PYTYPE_NM20070606_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/converter/registered.hpp>

namespace boost { namespace python { namespace converter {

template<PyTypeObject const* python_type>
struct wrap_pytype {
    static PyTypeObject const* get_pytype() { return python_type; }
};

#ifndef BOOST_PYTHON_NO_PY_SIGNATURES

namespace detail {
    template <class T>
    inline python::type_info unwind_type_id() {
        return python::type_id<cpp14::remove_pointer_t<cpp14::remove_reference_t<T>>>();
    }
}

template <class T>
struct expected_pytype_for_arg {
    static PyTypeObject const* get_pytype() {
        auto r = converter::registry::query(detail::unwind_type_id<T>());
        return r ? r->expected_from_python_type() : nullptr;
    }
};

template <class T>
struct registered_pytype {
    static PyTypeObject const *get_pytype() {
        auto r = converter::registry::query(detail::unwind_type_id<T>());
        return r ? r->m_class_object : nullptr;
    }
};

template <class T>
struct registered_pytype_direct {
    static PyTypeObject const* get_pytype() {
        return registered<T>::converters.m_class_object;
    }
};

template <class T>
struct expected_from_python_type : expected_pytype_for_arg<T>{};

template <class T>
struct expected_from_python_type_direct {
    static PyTypeObject const* get_pytype() {
        return registered<T>::converters.expected_from_python_type();
    }
};

template <class T>
struct to_python_target_type {
    static PyTypeObject const *get_pytype() {
        auto r = converter::registry::query(detail::unwind_type_id<T>());
        return r ? r->to_python_target_type() : nullptr;
    }
};

template <class T>
struct to_python_target_type_direct {
    static PyTypeObject const *get_pytype() {
        return registered<T>::converters.to_python_target_type();
    }
};

#endif // BOOST_PYTHON_NO_PY_SIGNATURES

}}} // namespace boost::python::converter

#endif // WRAP_PYTYPE_NM20070606_HPP
