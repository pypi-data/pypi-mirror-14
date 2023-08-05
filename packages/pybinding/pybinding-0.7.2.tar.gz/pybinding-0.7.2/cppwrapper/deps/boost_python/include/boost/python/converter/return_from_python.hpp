// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef RETURN_FROM_PYTHON_DWA200265_HPP
# define RETURN_FROM_PYTHON_DWA200265_HPP

# include <boost/python/converter/from_python.hpp>
# include <boost/python/converter/registered.hpp>
# include <boost/python/converter/object_manager.hpp>
# include <boost/python/errors.hpp>
# include <boost/python/handle.hpp>

namespace boost { namespace python { namespace converter { 

namespace detail {
    template<class T>
    struct return_lvalue_from_python {
        T operator()(PyObject* source) const {
            using from_python_t = lvalue_from_python<T>;

            // source is a new reference result from a function call.
            // It needs to be decrefed in all cases.
            handle<> decref_guard{source};

            if (source->ob_refcnt <= 1)
                from_python_t::throw_dangling_pointer();

            auto converter = from_python_t{source};
            if (!converter.check())
                from_python_t::throw_bad_conversion(source);

            return converter();
        };
    };

    template<class T>
    struct return_rvalue_from_python {
        T operator()(PyObject* source) {
            using from_python_t = rvalue_from_python<T>;

            // source is a new reference result from a function call.
            // It needs to be decrefed in all cases.
            handle<> decref_guard{source};

            auto converter = from_python_t{source};
            if (!converter.check()) {
                from_python_t::throw_bad_conversion(source);
            }

            return std::move(converter)();
        }
    };

    template<class T>
    struct return_object_manager_from_python {
        T operator()(PyObject* p) const {
            return static_cast<T>(
                object_manager_traits<T>::adopt(expect_non_null(p))
            );
        }
    };
} // namespace detail

template<class T>
struct return_from_python : cpp14::conditional_t<
    is_object_manager<T>::value,
    detail::return_object_manager_from_python<T>,
    cpp14::conditional_t<
        std::is_pointer<T>::value || std::is_lvalue_reference<T>::value,
        detail::return_lvalue_from_python<T>,
        detail::return_rvalue_from_python<T>
    >
> {};

// Specialization as a convenience for call and call_method
template<>
struct return_from_python<void> {
    void operator()(PyObject* p) const {
        decref(expect_non_null(p));
    }
};

}}} // namespace boost::python::converter

#endif // RETURN_FROM_PYTHON_DWA200265_HPP
