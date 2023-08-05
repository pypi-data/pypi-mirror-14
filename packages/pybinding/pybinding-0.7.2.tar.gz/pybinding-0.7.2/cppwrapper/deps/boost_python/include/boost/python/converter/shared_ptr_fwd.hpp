#pragma once
#include <boost/python/detail/prefix.hpp>

#ifdef BOOST_PYTHON_USE_STD_SHARED_PTR
# include <memory>
#else
# include <boost/shared_ptr.hpp>
#endif

namespace boost { namespace python { namespace converter {

#ifdef BOOST_PYTHON_USE_STD_SHARED_PTR
using std::shared_ptr;
using std::get_deleter;
#else
using boost::shared_ptr;
using boost::get_deleter;
#endif

template<class T>
struct is_shared_ptr : std::false_type {};

template<class T>
struct is_shared_ptr<shared_ptr<T>> : std::true_type {};

}}} // namespace boost::python::converter
