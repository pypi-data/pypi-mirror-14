// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef POINTER_HOLDER_DWA20011215_HPP
# define POINTER_HOLDER_DWA20011215_HPP 

# include <boost/python/instance_holder.hpp>
# include <boost/python/pointee.hpp>
# include <boost/python/type_id.hpp>

# include <boost/python/object/inheritance_query.hpp>

# include <boost/python/detail/get_pointer.hpp>
# include <boost/python/detail/wrapper_base.hpp>

namespace boost { namespace python {

template <class T> class wrapper;

namespace objects {

// Without back-reference
template<class Pointer, class Pointee, class = Pointee, bool has_back_reference = false>
struct pointer_holder : instance_holder {
    using value_type = Pointee;

    pointer_holder(Pointer p) : m_p(std::move(p)) {}

    template<class... Args>
    pointer_holder(PyObject* self, Args&&... args)
        : m_p(new Pointee(std::forward<Args>(args)...))
    {
        python::detail::initialize_wrapper(self, get_pointer(m_p));
    }

private: // required holder implementation
    virtual void* holds(type_info dst_t, bool null_ptr_only) final {
        if (dst_t == python::type_id<Pointer>() && !(null_ptr_only && get_pointer(m_p)))
            return &m_p;

        using non_const_pointee = cpp14::remove_const_t<Pointee>;
        auto p = const_cast<non_const_pointee*>(get_pointer(m_p));

        if (p == nullptr)
            return nullptr;

        if (auto wrapped = holds_wrapped(dst_t, p, p))
            return wrapped;

        auto src_t = python::type_id<Pointee>();
        return (src_t == dst_t) ? p : find_dynamic_type(p, src_t, dst_t);
    }

private:
    template<class T>
    static void* holds_wrapped(type_info dst_t, wrapper<T>*, T* p) {
        return python::type_id<T>() == dst_t ? p : nullptr;
    }
    
    static void* holds_wrapped(type_info, ...) {
        return nullptr;
    }

private:
    Pointer m_p;
};

// With back-reference
template<class Pointer, class Pointee, class Base>
struct pointer_holder<Pointer, Pointee, Base, true> : instance_holder {
    using value_type = Pointee;

    // Not sure about this one -- can it work? The source object
    // undoubtedly does not carry the correct back reference pointer.
    pointer_holder(Pointer p) : m_p(std::move(p)) {}

    template <class... Args>
    pointer_holder(PyObject* p, Args&&... args)
        : m_p(new Pointee(p, std::forward<Args>(args)...))
    {}

private: // required holder implementation
    virtual void* holds(type_info dst_t, bool null_ptr_only) final {
        if (dst_t == python::type_id<Pointer>() && !(null_ptr_only && get_pointer(m_p)))
            return &m_p;

        auto p = get_pointer(m_p);
        if (p == nullptr)
            return nullptr;

        if (dst_t == python::type_id<Pointee>())
            return p;

        auto src_t = python::type_id<Base>();
        return (src_t == dst_t) ? p : find_dynamic_type(p, src_t, dst_t);
    }

private:
    Pointer m_p;
};

}}} // namespace boost::python::objects

#endif // POINTER_HOLDER_DWA20011215_HPP
