// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef EXTRACT_DWA200265_HPP
# define EXTRACT_DWA200265_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/converter/object_manager.hpp>
# include <boost/python/converter/from_python.hpp>
# include <boost/python/converter/registered.hpp>

# include <boost/python/object_core.hpp>
# include <boost/python/refcount.hpp>

# include <boost/python/detail/copy_ctor_mutates_rhs.hpp>

namespace boost { namespace python {

namespace converter {
    template<class T>
    struct extract_lvalue : lvalue_from_python<T> {
        using base = lvalue_from_python<T>;
        using result_type = T;

        extract_lvalue(PyObject* source) : base{source}, source{source} {}

        T operator()() const {
            if (!base::check())
                base::throw_bad_conversion(source);

            return base::operator()();
        }

    private:
        PyObject* source;
    };

    template<class T>
    struct extract_rvalue : rvalue_from_python<T> {
        using base = rvalue_from_python<T>;
        using result_type = cpp14::conditional_t<
            python::detail::copy_ctor_mutates_rhs<T>::value,
            T&,
            T const&
        >;

        extract_rvalue(const extract_rvalue&) = delete;
        extract_rvalue& operator=(const extract_rvalue&) = delete;

        extract_rvalue(PyObject* source) : base{source} {}

        result_type operator()() & {
            if (!base::check())
                base::throw_bad_conversion(base::source);

            return base::operator()();
        }

        T operator()() && {
            if (!base::check())
                base::throw_bad_conversion(base::source);

            return std::move(base::operator()());
        }
    };

    template<class T>
    struct extract_object_manager {
        using result_type = T;

        extract_object_manager(PyObject* p) : m_source(p) {}

        bool check() const { return object_manager_traits<result_type>::check(m_source); }

        result_type operator()() const {
            return static_cast<result_type>(
                object_manager_traits<result_type>::adopt(incref(m_source))
            );
        }

    private:
        PyObject* m_source;
    };

    template<class T>
    using select_extract_t = cpp14::conditional_t<
        is_object_manager<T>::value,
        extract_object_manager<T>,
        cpp14::conditional_t<
            std::is_pointer<T>::value || std::is_lvalue_reference<T>::value,
            extract_lvalue<T>,
            extract_rvalue<T>
        >
    >;
} // namespace converter

template<class T>
struct extract : converter::select_extract_t<T> {
private:
    using base = converter::select_extract_t<T>;

public:
    using result_type = typename base::result_type;
    operator result_type() { return (*this)(); }
    
    extract(PyObject* p) : base(p) {}
    extract(object const& x) : base(x.ptr()) {}
};

}} // namespace boost::python::converter

#endif // EXTRACT_DWA200265_HPP
