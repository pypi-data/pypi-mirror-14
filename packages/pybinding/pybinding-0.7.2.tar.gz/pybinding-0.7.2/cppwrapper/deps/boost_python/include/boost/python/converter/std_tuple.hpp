#pragma once
#include <boost/python/converter/to_python_fwd.hpp>
#include <boost/python/converter/arg_from_python.hpp>

#include <boost/python/cpp14/utility.hpp>

#include <tuple>

namespace boost { namespace python { namespace converter {

template<class Tuple, class = cpp14::make_index_sequence<std::tuple_size<Tuple>::value>>
struct std_tuple_from_python;

template<template<class...> class Tuple, class... Ts, std::size_t... Is>
struct std_tuple_from_python<Tuple<Ts...>, cpp14::index_sequence<Is...>> {
    using tuple_t = Tuple<Ts...>;

    std_tuple_from_python() {
        registry::insert_implicit_rvalue_converter(
            &convertible, &construct, type_id<tuple_t>(), &PyTuple_Type
        );
    }

    static void* convertible(PyObject* source) {
        if (!PyTuple_Check(source))
            return nullptr;
        if (PyTuple_GET_SIZE(source) != sizeof...(Ts))
            return nullptr;

        for (bool check : {arg_from_python<Ts>{PyTuple_GET_ITEM(source, Is)}.check()..., true}) {
            if (!check)
                return nullptr;
        }

        return source;
    }

    static void construct(PyObject* source, rvalue_from_python_stage1_data* data) {
        void* storage = ((rvalue_from_python_storage<tuple_t>*)data)->storage.bytes;

        (void)source; // suppress GCC unused parameter warning when sizeof...(Ts) == 0
        new (storage) tuple_t(arg_from_python<Ts>{PyTuple_GET_ITEM(source, Is)}()...);

        data->convertible = storage;
    }
};

template<class... Ts>
struct rvalue_from_python_register<std::tuple<Ts...>> {
    static std_tuple_from_python<std::tuple<Ts...>> register_;

    rvalue_from_python_register() {
        [](...){}(register_); // trigger static initialization of std_tuple_from_python
    }
};

template<class... Ts>
std_tuple_from_python<std::tuple<Ts...>> rvalue_from_python_register<std::tuple<Ts...>>::register_;

template<class T1, class T2>
struct rvalue_from_python_register<std::pair<T1, T2>> {
    static std_tuple_from_python<std::pair<T1, T2>> register_;

    rvalue_from_python_register() { [](...){}(register_); }
};

template<class T1, class T2>
std_tuple_from_python<std::pair<T1, T2>> rvalue_from_python_register<std::pair<T1, T2>>::register_;

} // namespace converter

namespace detail {
    template<template<class...> class Tuple, class... Ts>
    struct to_python_tuple {
        PyObject* operator()(Tuple<Ts...> const& source) const {
            if (auto entry = converter::registry::query(type_id<Tuple<Ts...>>())) {
                if (entry->m_to_python)
                    return entry->m_to_python(&source);
            }

            return convert_impl(source, cpp14::make_index_sequence<sizeof...(Ts)>{});
        }

        template<std::size_t... Is>
        static PyObject* convert_impl(Tuple<Ts...> const& source, cpp14::index_sequence<Is...>) {
            return PyTuple_Pack(
                sizeof...(Ts), converter::arg_to_python<Ts>{std::get<Is>(source)}.get()...
            );
        }
    };
}

template<class... Ts>
struct to_python_value<std::tuple<Ts...>> : detail::to_python_tuple<std::tuple, Ts...> {};

template<class T1, class T2>
struct to_python_value<std::pair<T1, T2>> : detail::to_python_tuple<std::pair, T1, T2> {};

template<class... Ts>
struct to_python_pytype<std::tuple<Ts...>> {
    static PyTypeObject const* get() { return &PyTuple_Type; }
};

template<class T1, class T2>
struct to_python_pytype<std::pair<T1, T2>> {
    static PyTypeObject const* get() { return &PyTuple_Type; }
};

}} // namespace boost::python
