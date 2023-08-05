// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef TO_PYTHON_INDIRECT_DWA200221_HPP
# define TO_PYTHON_INDIRECT_DWA200221_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/object/pointer_holder.hpp>
# include <boost/python/object/make_ptr_instance.hpp>

# include <boost/python/detail/none.hpp>

# include <boost/python/refcount.hpp>

# include <memory>

namespace boost { namespace python {

template <class T, class MakeHolder>
struct to_python_indirect {
    template<class U>
    PyObject* operator()(U* ptr) const {
        return (ptr == nullptr) ? detail::none() : operator()(*ptr);
    }

    template<class U>
    PyObject* operator()(U const& x) const {
        if (std::is_polymorphic<U>::value) {
            if (auto owner = detail::wrapper_base_::owner(&x))
                return incref(owner);
        }
        return MakeHolder::execute(&x);
    }
};

namespace detail {
    struct make_owning_holder {
        template<class T>
        static PyObject* execute(T* p) {
            using smart_pointer = std::unique_ptr<T>;
            using holder_t = objects::pointer_holder<smart_pointer, T>;
            return objects::make_ptr_instance<T, holder_t>::execute(smart_pointer{p});
        }
    };

    struct make_reference_holder {
        template<class T>
        static PyObject* execute(T* p) {
            using holder_t = objects::pointer_holder<T*, T>;
            return objects::make_ptr_instance<T, holder_t>::execute(p);
        }
    };
}

}} // namespace boost::python

#endif // TO_PYTHON_INDIRECT_DWA200221_HPP
