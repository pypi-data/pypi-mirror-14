// Copyright David Abrahams 2001.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)

#ifndef MAKE_HOLDER_DWA20011215_HPP
# define MAKE_HOLDER_DWA20011215_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/object/instance.hpp>
# include <boost/python/detail/type_list.hpp>

namespace boost { namespace python { namespace objects {

template<class Class, class BasePolicy>
struct holder_policy : BasePolicy {
    holder_policy(BasePolicy base) : BasePolicy(base) {}

    template<class Signature>
    struct extract_signature;

    template<class... Args>
    struct extract_signature<python::detail::type_list<void, PyObject*, Args...>> {
        using type = python::detail::type_list<void, Class, Args...>;
    };
};

template<class Holder, class Sig>
struct make_holder;

template<class Holder, class... Args>
struct make_holder<Holder, detail::type_list<Args...>> {
    static void execute(PyObject* p, Args const&... args) {
        using instance_t = instance<Holder>;
        
        void* memory = Holder::allocate(p, offsetof(instance_t, storage), sizeof(Holder));
        try {
            // TODO: perfect forwarding
            (new (memory) Holder(p, args...))->install(p);
        }
        catch(...) {
            Holder::deallocate(p, memory);
            throw;
        }
    }
};

}}} // namespace boost::python::objects

# endif // MAKE_HOLDER_DWA20011215_HPP
