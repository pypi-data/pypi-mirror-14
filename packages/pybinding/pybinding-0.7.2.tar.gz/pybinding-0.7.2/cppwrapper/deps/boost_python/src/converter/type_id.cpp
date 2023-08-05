// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#include <boost/python/type_id.hpp>
#include <memory>

#ifdef BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE
# include <cxxabi.h>
#endif 

namespace boost { namespace python {

#ifdef BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE
namespace detail {
    BOOST_PYTHON_DECL std::string demangle(char const* mangled) {
        int status = -4;
        std::unique_ptr<char, void(*)(void*)> demangled{
            abi::__cxa_demangle(mangled, nullptr, nullptr, &status),
            std::free
        };
        assert(status != -3); // invalid argument error

        if (status == -1)
            throw std::bad_alloc();
        // In case of an invalid mangled name, the best we can do is to return it intact.
        return (status == 0) ? demangled.get() : mangled;
    }
}
#endif // BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE

BOOST_PYTHON_DECL std::ostream& operator<<(std::ostream& os, type_info const& x)
{
    return os << x.pretty_name();
}

}} // namespace boost::python
