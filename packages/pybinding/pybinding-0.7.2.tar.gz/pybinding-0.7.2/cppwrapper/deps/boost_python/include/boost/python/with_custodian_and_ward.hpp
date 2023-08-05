// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef WITH_CUSTODIAN_AND_WARD_DWA2002131_HPP
# define WITH_CUSTODIAN_AND_WARD_DWA2002131_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/default_call_policies.hpp>
# include <boost/python/object/life_support.hpp>

namespace boost { namespace python { 

template<std::size_t custodian, std::size_t ward, class BasePolicy = default_call_policies>
struct with_custodian_and_ward : BasePolicy {
    static_assert(custodian != ward, "");
    static_assert(custodian > 0, "");
    static_assert(ward > 0, "");

    template <class ArgumentPackage>
    static bool precall(ArgumentPackage const& args) {
        auto arity = static_cast<std::size_t>(args.arity());
        if (custodian > arity || ward > arity) {
            PyErr_SetString(
                PyExc_IndexError,
                "boost::python::with_custodian_and_ward: argument index out of range"
            );
            return false;
        }

        PyObject* patient = args.get(ward - 1);
        PyObject* nurse = args.get(custodian - 1);

        PyObject* life_support = python::objects::make_nurse_and_patient(nurse, patient);
        if (life_support == 0)
            return false;
    
        bool result = BasePolicy::precall(args);
        if (!result)
            decref(life_support);

        return result;
    }
};

template<std::size_t custodian, std::size_t ward, class BasePolicy = default_call_policies>
struct with_custodian_and_ward_postcall : BasePolicy {
    static_assert(custodian != ward, "");
    
    template <class ArgumentPackage>
    static PyObject* postcall(ArgumentPackage const& args, PyObject* result) {
        auto arity = static_cast<std::size_t>(args.arity());
        if (custodian > arity || ward > arity) {
            PyErr_SetString(
                PyExc_IndexError,
                "boost::python::with_custodian_and_ward_postcall: argument index out of range"
            );
            return nullptr;
        }
        
        PyObject* patient = (ward > 0) ? args.get(ward - 1) : result;
        PyObject* nurse = (custodian > 0) ? args.get(custodian - 1) : result;

        if (nurse == nullptr)
            return nullptr;

        result = BasePolicy::postcall(args, result);
        if (result == nullptr)
            return nullptr;

        if (python::objects::make_nurse_and_patient(nurse, patient) == nullptr) {
            xdecref(result);
            return nullptr;
        }

        return result;
    }
};


}} // namespace boost::python

#endif // WITH_CUSTODIAN_AND_WARD_DWA2002131_HPP
