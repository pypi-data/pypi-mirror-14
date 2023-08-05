#pragma once

namespace boost { namespace python {

namespace detail {
    template<class T>
    T* get_pointer(T* p) {
        return p;
    }

    template<class T>
    auto get_pointer(T const& p) -> decltype(p.get()) {
        return p.get();
    }
}

// it's needed in the main namespace for compatibility
using detail::get_pointer;

}} // namespace boost::python
