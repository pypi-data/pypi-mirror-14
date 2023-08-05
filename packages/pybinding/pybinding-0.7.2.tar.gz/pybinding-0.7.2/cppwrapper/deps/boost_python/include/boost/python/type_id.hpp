// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef TYPE_ID_DWA2002517_HPP
# define TYPE_ID_DWA2002517_HPP

# include <boost/python/detail/prefix.hpp>
# include <typeindex>
# include <ostream>
# include <string>

# ifndef BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE
#  if defined(__has_include)
#   if __has_include(<cxxabi.h>)
#    define BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE
#   endif
#  elif defined(__GLIBCXX__)
#   define BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE
#  endif
# endif

namespace boost { namespace python { namespace detail {
# ifdef BOOST_PYTHON_HAVE_GCC_CP_DEMANGLE
    BOOST_PYTHON_DECL std::string demangle(char const* name);
# else
    inline std::string demangle(char const* name) { return name; }
# endif
}}}

namespace boost { namespace python { 

// Type ids which represent the same information as std::type_index
// (i.e. the top-level reference and cv-qualifiers are stripped), but
// which have demangled names if supported.
// -> This should work across shared libraries on C++11 compilers.
struct type_info : std::type_index {
    using std::type_index::type_index;

    std::string pretty_name() const { return detail::demangle(name()); }

    friend BOOST_PYTHON_DECL std::ostream& operator<<(std::ostream&, type_info const&);
};

template <class T>
inline type_info type_id() { return {typeid(T)}; }

}} // namespace boost::python

#endif // TYPE_ID_DWA2002517_HPP
