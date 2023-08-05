#pragma once
#include <boost/python/converter/to_python_fwd.hpp>
#include <boost/python/converter/arg_from_python.hpp>

#include <unordered_map>

namespace boost { namespace python { namespace converter {

template<class UnorderedMap>
struct std_unordered_map_from_python;

template<class K, class V>
struct std_unordered_map_from_python<std::unordered_map<K, V>> {
    using Map = std::unordered_map<K, V>;

    std_unordered_map_from_python() {
        registry::insert_rvalue_converter(
            &convertible, &construct, type_id<Map>(), &PyDict_Type
        );
    }

    static void* convertible(PyObject* source) {
        if (!PyMapping_Check(source))
            return nullptr;

        auto keys = handle<>{allow_null(PyMapping_Keys(source))};
        if (!keys) {
            PyErr_Clear();
            return nullptr;
        }

        auto const size = PyMapping_Size(source);
        for (ssize_t i = 0; i < size; ++i) {
            if (!arg_from_python<K>{PyList_GET_ITEM(keys.get(), i)}.check())
                return nullptr;
        }

        auto values = handle<>{allow_null(PyMapping_Values(source))};
        if (!values) {
            PyErr_Clear();
            return nullptr;
        }

        for (ssize_t i = 0; i < size; ++i) {
            if (!arg_from_python<V>{PyList_GET_ITEM(values.get(), i)}.check())
                return nullptr;
        }

        return source;
    }

    static void construct(PyObject* source, rvalue_from_python_stage1_data* data) {
        void* storage = ((rvalue_from_python_storage<Map>*)data)->storage.bytes;

        new (storage) Map{};
        Map& map = *static_cast<Map*>(storage);

        auto const size = PyMapping_Size(source);
        auto keys = handle<>{allow_null(PyMapping_Keys(source))};
        auto values = handle<>{allow_null(PyMapping_Values(source))};

        for (ssize_t i = 0; i < size; ++i) {
            map.emplace(arg_from_python<K>{PyList_GET_ITEM(keys.get(), i)}(),
                        arg_from_python<V>{PyList_GET_ITEM(values.get(), i)}());
        }

        data->convertible = storage;
    }
};

template<class K, class V>
struct rvalue_from_python_register<std::unordered_map<K, V>> {
    static std_unordered_map_from_python<std::unordered_map<K, V>> register_;

    rvalue_from_python_register() {
        [](...){}(register_); // trigger static initialization of std_vector_from_python
    }
};

template<class K, class V>
std_unordered_map_from_python<std::unordered_map<K, V>>
    rvalue_from_python_register<std::unordered_map<K, V>>::register_;


} // namespace converter

template<class K, class V>
struct to_python_value<std::unordered_map<K, V>> {
    PyObject* operator()(std::unordered_map<K, V> const& source) const {
        // check for registry converters first (in case of user-defined converters)
        if (auto entry = converter::registry::query(type_id<std::unordered_map<K, V>>())) {
            if (entry->m_to_python)
                return entry->m_to_python(&source);
        }

        PyObject* dict = PyDict_New();
        for (auto const& pair : source) {
            PyDict_SetItem(dict, converter::arg_to_python<K>{pair.first}.get(),
                           converter::arg_to_python<V>{pair.second}.get());
        }
        return dict;
    }
};

template<class K, class V>
struct to_python_pytype<std::unordered_map<K, V>> {
    static PyTypeObject const* get() { return &PyDict_Type; }
};


}} // namespace boost::python
