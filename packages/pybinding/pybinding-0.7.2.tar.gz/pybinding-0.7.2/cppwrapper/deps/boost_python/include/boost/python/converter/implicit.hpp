// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef IMPLICIT_DWA2002326_HPP
# define IMPLICIT_DWA2002326_HPP

# include <boost/python/converter/rvalue_from_python_data.hpp>
# include <boost/python/converter/registrations.hpp>
# include <boost/python/converter/registered.hpp>

# include <boost/python/extract.hpp>

namespace boost { namespace python { namespace converter { 

template <class Source, class Target>
struct implicit
{
    static void* convertible(PyObject* obj)
    {
        // Find a converter which can produce a Source instance from
        // obj. The user has told us that Source can be converted to
        // Target, and instantiating construct() below, ensures that
        // at compile-time.
        return implicit_rvalue_convertible_from_python(obj, registered<Source>::converters)
            ? obj : 0;
    }
      
    static void construct(PyObject* obj, rvalue_from_python_stage1_data* data)
    {
        void* storage = ((rvalue_from_python_storage<Target>*)data)->storage.bytes;

        construct_impl(storage, obj, std::is_abstract<Source>{});
        
        // record successful construction
        data->convertible = storage;
    }

private:
    static void construct_impl(void* storage, PyObject* p, std::true_type /*is_abstract*/) {
        arg_from_python<Source const&> get_source(p);
        assert(get_source.check());
        new (storage) Target(get_source());
    }

    static void construct_impl(void* storage, PyObject* p, std::false_type /*is_abstract*/) {
        arg_from_python<Source> get_source(p);
        assert(get_source.check());
        new (storage) Target(std::move(get_source)());
    }
};

}}} // namespace boost::python::converter

#endif // IMPLICIT_DWA2002326_HPP
