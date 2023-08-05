// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef RETURN_INTERNAL_REFERENCE_DWA2002131_HPP
# define RETURN_INTERNAL_REFERENCE_DWA2002131_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/default_call_policies.hpp>
# include <boost/python/reference_existing_object.hpp>
# include <boost/python/with_custodian_and_ward.hpp>

namespace boost { namespace python { 

template<std::size_t owner_arg = 1, class BasePolicy = default_call_policies>
struct return_internal_reference
    : with_custodian_and_ward_postcall<0, owner_arg, BasePolicy>
{
    static_assert(owner_arg > 0, "The result can't own itself");
    using result_converter = reference_existing_object;
};

}} // namespace boost::python

#endif // RETURN_INTERNAL_REFERENCE_DWA2002131_HPP
