// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef STR_20020703_HPP
#define STR_20020703_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/object.hpp>
# include <boost/python/list.hpp>
# include <boost/python/converter/pytype_object_mgr_traits.hpp>

// disable defines in <cctype> provided by some system libraries
#undef isspace
#undef islower
#undef isalpha
#undef isdigit
#undef isalnum
#undef isupper

namespace boost { namespace python {

class str : public object {
public:
    str(char const* s = "")
        : object{detail::new_reference(BOOST_PyString_FromString(s))}
    {}

    str(char const* start, char const* finish)
        : object{detail::new_reference(
            BOOST_PyString_FromStringAndSize(start, str_size_as_py_ssize_t(finish - start))
        )}
    {}

    str(char const* start, std::size_t length)
        : object{detail::new_reference(
            BOOST_PyString_FromStringAndSize(start, str_size_as_py_ssize_t(length))
        )}
    {}

    template<class T>
    explicit str(T&& other)
        : str{call(object{std::forward<T>(other)})}
    {}

public:
    str capitalize() const { return str_call("capitalize"); }

#if PY_MAJOR_VERSION >= 3 && PY_MINOR_VERSION >= 3
    str casefold() const { return str_call("casefold"); }
#endif

    template<class T, class... Os>
    str center(T&& width, Os&&... fillchar) const {
        static_assert(sizeof...(Os) <= 1, "width[, fillchar]");
        return str_call("center", std::forward<T>(width), std::forward<Os>(fillchar)...);
    }

    template<class T, class... Os>
    long count(T&& sub, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return int_call("count", std::forward<T>(sub), std::forward<Os>(start_end)...);
    }

#if PY_MAJOR_VERSION < 3
    template<class... Os>
    object decode(Os&&... encoding_errors) const {
        static_assert(sizeof...(Os) <= 2, "");
        return attr("decode")(std::forward<Os>(encoding_errors)...);
    }
#endif

    template<class... Os>
    object encode(Os&&... encoding_errors) const {
        static_assert(sizeof...(Os) <= 2, "");
        return attr("encode")(std::forward<Os>(encoding_errors)...);
    }

    template<class T, class... Os>
    bool endswith(T&& suffix, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return bool_call("endswith", std::forward<T>(suffix), std::forward<Os>(start_end)...);
    }

    template<class... Os>
    str expandtabs(Os&&... tabsize) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("expandtabs", std::forward<Os>(tabsize)...);
    }

    template<class T, class... Os>
    long find(T&& sub, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return int_call("find", std::forward<T>(sub), std::forward<Os>(start_end)...);
    }

    template <class... Ts>
    str format(Ts&&... args) const {
        return str_call("format", std::forward<Ts>(args)...);
    }

    str format(detail::kwargs_proxy kwargs) {
        return str{attr("format")(kwargs)};
    };

#if PY_MAJOR_VERSION >= 3 && PY_MINOR_VERSION >= 2
    template <class T>
    str format_map(T&& mapping) const {
        return str_call("format_map", std::forward<T>(mapping));
    }
#endif

    template<class T, class... Os>
    long index(T&& sub, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return int_call("index", std::forward<T>(sub), std::forward<Os>(start_end)...);
    }

    bool isalnum() const { return bool_call("isalnum"); }
    bool isalpha() const { return bool_call("isalpha"); }
    bool isdigit() const { return bool_call("isdigit"); }
#if PY_MAJOR_VERSION >= 3
    bool isidentifier() const { return bool_call("isidentifier"); }
#endif
    bool islower() const { return bool_call("islower"); }
#if PY_MAJOR_VERSION >= 3
    bool isnumeric() const { return bool_call("isnumeric"); }
    bool isprintable() const { return bool_call("isprintable"); }
#endif
    bool isspace() const { return bool_call("isspace"); }
    bool istitle() const { return bool_call("istitle"); }
    bool isupper() const { return bool_call("isupper"); }

    template<class T>
    str join(T&& sequence) const {
        return str_call("join", std::forward<T>(sequence));
    }

    template <class T, class... Os>
    str ljust(T&& width, Os&&... fillchar) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("ljust", std::forward<T>(width), std::forward<Os>(fillchar)...);
    }

    str lower() const { return str_call("lower"); }

    template<class... Os>
    str lstrip(Os&&... chars) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("lstrip", std::forward<Os>(chars)...);
    }

#if PY_MAJOR_VERSION >= 3
    template<class... Os>
    str maketrans(Os&&... x_y_z) const {
        static_assert(sizeof...(Os) <= 3, "");
        return str_call("maketrans", std::forward<Os>(x_y_z)...);
    }
#endif

    template <class T>
    str partition(T&& sep) const {
        return str_call("partition", std::forward<T>(sep));
    }

    template <class T1, class T2, class... Os>
    str replace(T1&& old, T2&& new_, Os&&... maxsplit) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("replace", std::forward<T1>(old), std::forward<T2>(new_),
                        std::forward<Os>(maxsplit)...);
    }
    
    template <class T, class... Os>
    long rfind(T&& sub, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return int_call("rfind", std::forward<T>(sub), std::forward<Os>(start_end)...);
    }

    template <class T, class... Os>
    long rindex(T&& sub, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return int_call("rindex", std::forward<T>(sub), std::forward<Os>(start_end)...);
    }

    template <class T, class... Os>
    str rjust(T&& width, Os&&... fillchar) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("rjust", std::forward<T>(width), std::forward<Os>(fillchar)...);
    }

    template <class T>
    str rpartition(T&& sep) const {
        return str_call("rpartition", std::forward<T>(sep));
    }

    template<class... Os>
    list rsplit(Os&&... sep_maxsplit) const {
        static_assert(sizeof...(Os) <= 2, "");
        return list{attr("rsplit")(std::forward<Os>(sep_maxsplit)...)};
    };

    template<class... Os>
    str rstrip(Os&&... chars) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("rstrip", std::forward<Os>(chars)...);
    }

    template<class... Os>
    list split(Os&&... sep_maxsplit) const {
        static_assert(sizeof...(Os) <= 2, "");
        return list{attr("split")(std::forward<Os>(sep_maxsplit)...)};
    };

    template<class... Os>
    list splitlines(Os&&... keepends) const {
        static_assert(sizeof...(Os) <= 1, "");
        return list{attr("splitlines")(std::forward<Os>(keepends)...)};
    };

    template<class T, class... Os>
    bool startswith(T&& prefix, Os&&... start_end) const {
        static_assert(sizeof...(Os) <= 2, "");
        return bool_call("startswith", std::forward<T>(prefix), std::forward<Os>(start_end)...);
    }

    template<class... Os>
    str strip(Os&&... chars) const {
        static_assert(sizeof...(Os) <= 1, "");
        return str_call("strip", std::forward<Os>(chars)...);
    }

    str swapcase() const { return str_call("swapcase"); }
    str title() const { return str_call("title"); }

    template<class T, class... Os>
    str translate(T&& table, Os&&... deletechars) const {
        return str_call("translate", std::forward<T>(table), std::forward<Os>(deletechars)...);
    }

    str upper() const { return str_call("upper"); }

    template <class T>
    str zfill(T&& width) const {
        return str_call("zfill", std::forward<T>(width));
    }

public: // implementation detail -- for internal use only
    BOOST_PYTHON_FORWARD_OBJECT_CONSTRUCTORS(str, object)

private:
    static detail::new_reference call(object const& arg) {
        return detail::new_reference(
            PyObject_CallFunctionObjArgs((PyObject*)&BOOST_PyString_Type, arg.ptr(), nullptr)
        );
    }

    template<class... Args>
    str str_call(char const* name, Args&&... args) const {
        return str{detail::new_reference(
            PyObject_CallMethodObjArgs(
                ptr(),
                handle<>{BOOST_PyString_FromString(name)}.get(),
                object{std::forward<Args>(args)}.ptr()...,
                nullptr
            )
        )};
    };

    template<class... Args>
    long int_call(char const* name, Args&&... args) const {
        auto o = object{detail::new_reference(
            PyObject_CallMethodObjArgs(
                ptr(),
                handle<>{BOOST_PyString_FromString(name)}.get(),
                object{std::forward<Args>(args)}.ptr()...,
                nullptr
            )
        )};

        long result = BOOST_PyInt_AsLong(o.ptr());
        if (PyErr_Occurred())
            throw_error_already_set();
        return result;
    }

    template<class... Args>
    bool bool_call(char const* name, Args&&... args) const {
        return int_call(name, std::forward<Args>(args)...) != 0;
    }


    static ssize_t str_size_as_py_ssize_t(std::size_t n) {
        if (n > static_cast<std::size_t>(ssize_t_max)) {
            throw std::range_error("str size > ssize_t_max");
        }
        return static_cast<ssize_t>(n);
    }
};

//
// Converter Specializations
//
namespace converter {
  template <>
  struct object_manager_traits<str>
      : pytype_object_manager_traits<&BOOST_PyString_Type, str>
  {};
}

inline namespace literals {
    inline str operator"" _s(char const* c_str, std::size_t) {
        return str{c_str};
    }
}

}}  // namespace boost::python

#endif // STR_20020703_HPP
