#pragma once
#include <boost/python/converter/to_python_fwd.hpp>
#include <boost/python/converter/arg_from_python.hpp>

#include <vector>

namespace boost { namespace python { namespace converter {

template<class Vector>
struct std_vector_from_python;

template<class T>
struct std_vector_from_python<std::vector<T>> {
    std_vector_from_python() {
        registry::insert_rvalue_converter(
            &convertible, &construct, type_id<std::vector<T>>(), &PyList_Type
        );
    }

    static void* convertible(PyObject* source) {
        auto sequence = handle<>{allow_null(PySequence_Fast(source, ""))};
        if (!sequence) {
            PyErr_Clear();
            return nullptr;
        }

        auto const size = PySequence_Fast_GET_SIZE(sequence.get());
        for (ssize_t i = 0; i < size; ++i) {
            if (!arg_from_python<T>{PySequence_Fast_GET_ITEM(sequence.get(), i)}.check())
                return nullptr;
        }

        return source;
    }

    static void construct(PyObject* source, rvalue_from_python_stage1_data* data) {
        void* storage = ((rvalue_from_python_storage<std::vector<T>>*)data)->storage.bytes;

        auto sequence = handle<>{allow_null(PySequence_Fast(source, ""))};
        auto const size = PySequence_Fast_GET_SIZE(sequence.get());

        new (storage) std::vector<T>(size);
        std::vector<T>& v = *static_cast<std::vector<T>*>(storage);

        for (ssize_t i = 0; i < size; ++i) {
            v[i] = arg_from_python<T>{PySequence_Fast_GET_ITEM(sequence.get(), i)}();
        }

        data->convertible = storage;
    }
};

template<class T>
struct rvalue_from_python_register<std::vector<T>> {
    static std_vector_from_python<std::vector<T>> register_;

    rvalue_from_python_register() {
        [](...){}(register_); // trigger static initialization of std_vector_from_python
    }
};

template<class T>
std_vector_from_python<std::vector<T>> rvalue_from_python_register<std::vector<T>>::register_;

} // namespace converter

template<class T>
struct to_python_value<std::vector<T>> {
    PyObject* operator()(std::vector<T> const& source) const {
        // check for registry converters first (e.g. vector_indexing_suite)
        if (auto entry = converter::registry::query(type_id<std::vector<T>>())) {
            if (entry->m_to_python)
                return entry->m_to_python(&source);
        }

        auto const size = static_cast<ssize_t>(source.size());
        PyObject* list = PyList_New(size);
        for (ssize_t i = 0; i < size; ++i) {
            PyList_SET_ITEM(list, i, converter::arg_to_python<T>{source[i]}.release());
        }
        return list;
    }
};

template<class T>
struct to_python_pytype<std::vector<T>> {
    static PyTypeObject const* get() { return &PyList_Type; }
};

}} // namespace boost::python
