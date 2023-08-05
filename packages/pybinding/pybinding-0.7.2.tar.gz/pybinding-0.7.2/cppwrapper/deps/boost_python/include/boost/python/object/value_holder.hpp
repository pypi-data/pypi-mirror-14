// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

# ifndef VALUE_HOLDER_DWA20011215_HPP
#  define VALUE_HOLDER_DWA20011215_HPP 

# include <boost/python/instance_holder.hpp>
# include <boost/python/type_id.hpp>
# include <boost/python/wrapper.hpp>

# include <boost/python/object/inheritance_query.hpp>

namespace boost { namespace python { namespace objects {

// Without back-reference
template<class Value, class = Value, bool has_back_reference = false>
struct value_holder : instance_holder {
    using value_type = Value;

    template<class... Args>
    value_holder(PyObject* self, Args&&... args)
        : m_held(std::forward<Args>(args)...)
    {
        python::detail::initialize_wrapper(self, std::addressof(m_held));
    }

private: // required holder implementation
    virtual void* holds(type_info dst_t, bool /*null_ptr_only*/) final {
        auto p = std::addressof(m_held);
        if (auto wrapped = holds_wrapped(dst_t, p, p))
            return wrapped;

        auto src_t = python::type_id<Value>();
        return (src_t == dst_t) ? p : find_static_type(p, src_t, dst_t);
    }

private:
    template <class T>
    static void* holds_wrapped(type_info dst_t, wrapper<T>*, T* p) {
        return python::type_id<T>() == dst_t ? p : nullptr;
    }
    
    static void* holds_wrapped(type_info, ...) {
        return nullptr;
    }

private:
    Value m_held;
};

// With back-reference
template<class Value, class Held>
struct value_holder<Value, Held, true> : instance_holder {
    using value_type = Value;
    
    template <class... Args>
    value_holder(PyObject* p, Args&&... args)
        : m_held(p, std::forward<Args>(args)...)
    {}

private: // required holder implementation
    virtual void* holds(type_info dst_t, bool /*null_ptr_only*/) final {
        auto p = &m_held;
        auto src_t = python::type_id<Value>();

        if (dst_t == src_t || dst_t == python::type_id<Held>())
            return p;
        else
            return find_static_type(p, src_t, dst_t);
    }

private:
    Held m_held;
};

}}} // namespace boost::python::objects

# endif // VALUE_HOLDER_DWA20011215_HPP
