// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef FIND_FROM_PYTHON_DWA2002223_HPP
# define FIND_FROM_PYTHON_DWA2002223_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/converter/rvalue_from_python_data.hpp>

# include <boost/python/converter/registered.hpp>
# include <boost/python/errors.hpp>

namespace boost { namespace python { namespace converter { 

BOOST_PYTHON_DECL
void* get_lvalue_from_python(PyObject* source, registration const&);

BOOST_PYTHON_DECL bool implicit_rvalue_convertible_from_python(PyObject* source,
                                                               registration const&);

BOOST_PYTHON_DECL rvalue_from_python_stage1_data rvalue_from_python_stage1(PyObject* source,
                                                                           registration const&);

namespace errors {
    BOOST_PYTHON_DECL
    void throw_dangling_pointer(registration const&, char const* ref_type);

    BOOST_PYTHON_DECL
    void throw_bad_lvalue_conversion(PyObject* source, registration const&, char const* ref_type);

    BOOST_PYTHON_DECL
    void throw_bad_rvalue_conversion(PyObject* source, registration const&);
};

// lvalue converters
//
//   These require that an lvalue of the type U is stored somewhere in
//   the Python object being converted.
//
template<class T>
struct lvalue_from_python;

template<class T>
struct lvalue_from_python<T*> {
    lvalue_from_python(PyObject* source)
        : result{(source == Py_None)
                 ? source
                 : get_lvalue_from_python(source, registered<T>::converters)}
    {}

    bool check() const { return result != nullptr; }

    T* operator()() const {
        return (result == Py_None) ? nullptr : static_cast<T*>(result);
    }

public:
    static void throw_dangling_pointer() {
        errors::throw_dangling_pointer(registered<T>::converters, "pointer");
    }

    static void throw_bad_conversion(PyObject* source) {
        errors::throw_bad_lvalue_conversion(source, registered<T>::converters, "pointer");
    }

private:
    void* result;
};

template<class T>
struct lvalue_from_python<T&> {
    lvalue_from_python(PyObject* source)
        : result{get_lvalue_from_python(source, registered<T>::converters)}
    {}

    bool check() const { return result != nullptr; }

    T& operator()() const {
        return python::detail::void_ptr_to_reference<T>(result);
    }

public:
    static void throw_dangling_pointer() {
        errors::throw_dangling_pointer(registered<T>::converters, "reference");
    }

    static void throw_bad_conversion(PyObject* source) {
        errors::throw_bad_lvalue_conversion(source, registered<T>::converters, "reference");
    }

private:
    void* result;
};

// register rvalue
//
//   Used to register rvalue converters at 'def' calls (when function signatures are read).
//   This is useful for template types like std::tuple. A specialization should be provided
//   with the necessary converter registration. See 'std::tuple.hpp' for an example.
//   Note: This is not ideal, but needed for now because pytype information is runtime data
//   which must be initialized before anything else.
//
template<class T>
struct rvalue_from_python_register {};

// rvalue converters
//
//   These require only that an object of type T can be created from
//   the given Python object, but not that the T object exist somewhere in storage.
//
template<class T>
struct rvalue_from_python_base : rvalue_from_python_register<T> {
    rvalue_from_python_base(PyObject* source)
        : source{source},
          data{rvalue_from_python_stage1(source, registered<T>::converters)}
    {}

    bool check() const { return data.stage1.convertible != nullptr; }

public:
    static void throw_bad_conversion(PyObject* source) {
        errors::throw_bad_rvalue_conversion(source, registered<T>::converters);
    }

protected:
    T& stage2_conversion() {
        // Only do the stage2 conversion once
        if (data.stage1.convertible != data.storage.bytes && data.stage1.construct)
            data.stage1.construct(source, &data.stage1);

        return python::detail::void_ptr_to_reference<T>(data.stage1.convertible);
    }

    bool result_is_temp_object() const {
        return data.stage1.convertible == data.storage.bytes;
    }

protected:
    PyObject* source;
    rvalue_from_python_data<T> data;
};

template<class T>
struct rvalue_from_python : rvalue_from_python_base<T> {
    using base = rvalue_from_python_base<T>;
    using base::base;

    T& operator()() & { return base::stage2_conversion(); }

    T operator()() && {
        auto& result = base::stage2_conversion();
        if (base::result_is_temp_object()) {
            // When the result is a temp object stored in data.storage.bytes,
            // it should be moved out whenever possible.
            // Note: This will be a copy if T's move constructor was deleted
            // by the compiler. However, there will be a compile error if T's
            // move constructor was explicitly deleted: 'T(T&&) = delete;'.
            // Unfortunately, std::is_move_constructible cannot detect this
            // case, so this is an open issue for now.
            return std::move(result);
        }
        else {
            // When the result is a pointer to embedded data in a Python object,
            // it should be copied out. This may not be possible for move-only
            // types (e.g. std::unique_ptr), in which case the value is moved,
            // thus stealing the data from the Python object.
            return maybe_copy(result, std::is_copy_constructible<T>{});
        }
    }

private:
    T&  maybe_copy(T& result, std::true_type) { return result; }
    T&& maybe_copy(T& result, std::false_type) { return std::move(result); }
};

// T const& is a special rvalue case where operator() should always return a reference.
// This eliminates the temp value creation overhead of 'T operator()() &&'.
template<class T>
struct rvalue_from_python<T const&> : rvalue_from_python_base<T> {
    using base = rvalue_from_python_base<T>;
    using base::base;

    T const& operator()() { return base::stage2_conversion(); }
};

}}} // namespace boost::python::converter

#endif // FIND_FROM_PYTHON_DWA2002223_HPP
