// Copyright David Abrahams 2004. Distributed under the Boost
// Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#ifndef WRAPPER_BASE_DWA2004722_HPP
# define WRAPPER_BASE_DWA2004722_HPP

# include <boost/python/detail/prefix.hpp>
# include <type_traits>

namespace boost { namespace python {

class override;

namespace detail {

class BOOST_PYTHON_DECL wrapper_base {
public:
    PyObject* owner() const volatile { return m_self; }

protected:
    wrapper_base() = default;

    override get_override(char const* name, PyTypeObject* class_object) const;

private:
    PyObject* m_self = nullptr;

    friend void initialize_wrapper(PyObject* self, wrapper_base* w);
};

namespace wrapper_base_ // ADL disabler
{
    inline PyObject* owner_impl(void const volatile* /*x*/, std::false_type) {
        return nullptr;
    }

    template <class T>
    inline PyObject* owner_impl(T const volatile* x, std::true_type) {
        if (auto w = dynamic_cast<wrapper_base const volatile*>(x)) {
            return w->owner();
        }
        return nullptr;
    }

    template <class T>
    inline PyObject* owner(T const volatile* x) {
        return wrapper_base_::owner_impl(x, std::is_polymorphic<T>());
    }
} // namespace wrapper_base_

inline void initialize_wrapper(PyObject* self, wrapper_base* w) {
    w->m_self = self;
}

inline void initialize_wrapper(PyObject* /*self*/, ...) {}

}}} // namespace boost::python::detail

#endif // WRAPPER_BASE_DWA2004722_HPP
