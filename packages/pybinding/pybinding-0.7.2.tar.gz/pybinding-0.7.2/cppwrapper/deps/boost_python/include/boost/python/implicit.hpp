// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef IMPLICIT_DWA2002325_HPP
# define IMPLICIT_DWA2002325_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/converter/implicit.hpp>
# include <boost/python/converter/registry.hpp>
# include <boost/python/type_id.hpp>

namespace boost { namespace python { 

template <class Source, class Target>
void implicitly_convertible()
{
    typedef converter::implicit<Source,Target> functions;
    
    converter::registry::insert_implicit_rvalue_converter(
        &functions::convertible,
        &functions::construct,
        type_id<Target>(),
        nullptr,
        &converter::registry::lookup(type_id<Source>())
    );
}

}} // namespace boost::python

#endif // IMPLICIT_DWA2002325_HPP
