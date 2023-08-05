// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef CLASS_DWA200216_HPP
# define CLASS_DWA200216_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/class_fwd.hpp>
# include <boost/python/object/class.hpp>

# include <boost/python/object.hpp>
# include <boost/python/type_id.hpp>
# include <boost/python/data_members.hpp>
# include <boost/python/make_function.hpp>
# include <boost/python/signature.hpp>
# include <boost/python/init.hpp>
# include <boost/python/args_fwd.hpp>

# include <boost/python/object/class_metadata.hpp>
# include <boost/python/object/pickle_support.hpp>
# include <boost/python/object/add_to_namespace.hpp>

# include <boost/python/detail/overloads_fwd.hpp>
# include <boost/python/detail/operator_id.hpp>
# include <boost/python/detail/def_helper.hpp>
# include <boost/python/detail/unwrap_wrapper.hpp>

namespace boost { namespace python {

template <class DerivedVisitor> class def_visitor;

enum no_init_t { no_init };

// This is the primary mechanism through which users will expose C++ classes to Python.
// W is the class being wrapped. Args are arbitrarily-ordered optional arguments.
template<class W, class... Args>
class class_ : public objects::class_base {
    static_assert(sizeof...(Args) <= 3, "Maximum of 3 optional arguments");

public:
    using base = objects::class_base;
    using self = class_<W, Args...>;
    using metadata = typename objects::class_metadata<W, Args...>;
    using wrapped_type = W;

private:
    // A helper class which will contain an array of id objects to be
    // passed to the base class constructor
    template<class BasesPack>
    struct id_vector_impl;
    
    template<class... Bases>
    struct id_vector_impl<bases<Bases...>> {
        id_vector_impl() : ids{type_id<detail::unwrap_wrapper_t<W>>(), type_id<Bases>()...} {}
		std::vector<type_info> ids;
    };

    using id_vector = id_vector_impl<typename metadata::base_list>;

public:
    // Construct with default __init__() function
    class_(char const* name, char const* docstring = nullptr)
        : class_{name, docstring, init<>{}}
    {}

    // Construct with init<> function
    template<class Derived>
    class_(char const* name, init_base<Derived> const& init_function)
        : class_{name, nullptr, init_function}
    {}

    template<class Derived>
    class_(char const* name, char const* docstring, init_base<Derived> const& init_function)
        : base(name, id_vector{}.ids, docstring)
    {
        metadata::register_(); // set up runtime metadata/conversions
        base::set_instance_size(objects::additional_instance_size<typename metadata::holder>::value);
        def(init_function);
    }

    // Construct with uncallable __init__ function
    class_(char const* name, no_init_t)
        : class_{name, nullptr, no_init}
    {}

    class_(char const* name, char const* docstring, no_init_t)
        : base{name, id_vector{}.ids, docstring}
    {
        metadata::register_(); // set up runtime metadata/conversions
        base::def_no_init();
    }

public:
    // Wrap a member function or a non-member function which can take
    // a T, T cv&, or T cv* as its first parameter, a callable
    // python object, or a generic visitor.
    template<class Function>
    self& def(char const* name, Function f) {
        def_impl(name, f, detail::def_helper<char const*>(nullptr), &f);
        return *this;
    }

    template<class Function, class MaybeOverloads>
    self& def(char const* name, Function f, MaybeOverloads const& mo) {
        def_maybe_overloads(name, f, mo, &mo);
        return *this;
    }

    template<class Function, class A1, class A2>
    self& def(char const* name, Function f, A1 const& a1, A2 const& a2) {
        def_impl(name, f, detail::make_def_helper(a1, a2), &f);
        return *this;
    }

    template<class Function, class A1, class A2, class A3>
    self& def(char const* name, Function f, A1 const& a1, A2 const& a2, A3 const& a3) {
        def_impl(name, f, detail::make_def_helper(a1, a2, a3), &f);
        return *this;
    }

    // Generic visitation
    template<class Derived>
    self& def(def_visitor<Derived> const& visitor) {
        visitor.visit(*this);
        return *this;
    }

    self& staticmethod(char const* name) {
        make_method_static(name);
        return *this;
    }

public: // Data member access
    template<class D, class B>
    self& def_readonly(char const* name, D B::*pm, char const* docstring = nullptr) {
        return add_property(name, pm, docstring);
    }

    template<class D>
    self& def_readonly(char const* name, D const& d, char const* = nullptr) {
        return add_static_property(name, python::make_getter(d));
    }

    template<class D, class B>
    self& def_readwrite(char const* name, D B::*pm, char const* docstring = nullptr) {
        return add_property(name, pm, pm, docstring);
    }

    template <class D>
    self& def_readwrite(char const* name, D&& d, char const* = nullptr) {
        return add_static_property(name, python::make_getter(d), python::make_setter(d));
    }

public: // Property creation
    template<class Get>
    self& add_property(char const* name, Get fget, char const* docstring = nullptr) {
        base::add_property(name, make_getter_for_this(fget), docstring);
        return *this;
    }

    template<class Get, class Set>
    self& add_property(char const* name, Get fget, Set fset, char const* docstring = nullptr) {
        base::add_property(name, make_getter_for_this(fget), make_setter_for_this(fset), docstring);
        return *this;
    }

    template<class Get>
    self& add_static_property(char const* name, Get fget) {
        base::add_static_property(name, object(fget));
        return *this;
    }

    template<class Get, class Set>
    self& add_static_property(char const* name, Get fget, Set fset) {
        base::add_static_property(name, object(fget), object(fset));
        return *this;
    }

    template<class U>
    self& setattr(char const* name, U const& x) {
        base::setattr(name, object(x));
        return *this;
    }

public: // Pickle support
    template<class PickleSuiteType>
    self& def_pickle(PickleSuiteType const&) {
        static_assert(std::is_base_of<pickle_suite, PickleSuiteType>::value, "");

        detail::pickle_suite_finalize<PickleSuiteType>::register_(
            *this,
            &PickleSuiteType::getinitargs,
            &PickleSuiteType::getstate,
            &PickleSuiteType::setstate,
            PickleSuiteType::getstate_manages_dict()
        );
        return *this;
    }

    self& enable_pickling() {
        base::enable_pickling_(false);
        return *this;
    }

private:
    // Builds a method for this class around the given [member]
    // function pointer or object, appropriately adjusting the type of
    // the first signature argument so that if f is a member of a
    // (possibly not wrapped) base class of T, an lvalue argument of
    // type T will be required.
    template<class F>
    object make_getter_for_this(F f) {
        using is_obj_or_proxy = typename api::is_object_operators<F>::type;
        using unwrapped = detail::unwrap_wrapper_t<W>;

        return make_fn_impl<unwrapped>(
            f, is_obj_or_proxy{}, std::is_member_object_pointer<F>{}, std::true_type{}
        );
    }
    
    template<class F>
    object make_setter_for_this(F f) {
        using is_obj_or_proxy = typename api::is_object_operators<F>::type;
        using unwrapped = detail::unwrap_wrapper_t<W>;
        
        return make_fn_impl<unwrapped>(
            f, is_obj_or_proxy{}, std::is_member_object_pointer<F>{}, std::false_type{}
        );
    }
    
    template<class T, class F>
    object make_fn_impl(F const& f, std::false_type /*is_object*/,
                        std::false_type /*is_member*/, ...)
    {
        return python::make_function(f, default_call_policies{}, detail::get_signature_t<F, T>{});
    };

    template <class T, class D, class B>
    object make_fn_impl(D B::*pm, std::false_type /*is_object*/,
                        std::true_type /*is_member*/, std::true_type /*is_getter*/)
    {
        return python::make_getter(static_cast<D T::*>(pm));
    }

    template <class T, class D, class B>
    object make_fn_impl(D B::*pm, std::false_type /*is_object*/,
                        std::true_type /*is_member*/, std::false_type /*is_getter*/)
    {
        return python::make_setter(static_cast<D T::*>(pm));
    }

    template <class T, class F>
    object make_fn_impl(F x, std::true_type /*is_object*/, std::false_type /*is_member*/, ...) {
        return x;
    }

private:
    // These two overloads discriminate between def() as applied to a
    // generic visitor and everything else.
    template<class Helper, class _, class Visitor>
    void def_impl(char const* name, _, Helper const& helper, def_visitor<Visitor> const* v) {
        v->visit(*this, name,  helper);
    }

    template<class Function, class Helper>
    void def_impl(char const* name, Function f, Helper const& helper, ...) {
        using target = detail::unwrap_wrapper_t<W>;
        objects::add_to_namespace(
            *this, name,
            make_function(f, helper.policies(), helper.keywords(),
                          detail::get_signature_t<Function, target>{}),
            helper.doc()
        );

        def_default<Function>(name, helper,
                              std::integral_constant<bool, Helper::has_default_implementation>{});
    }

    //
    // These two overloads handle the definition of default
    // implementation overloads for virtual functions. The second one
    // handles the case where no default implementation was specified.
    template<class Function, class Helper>
    void def_default(char const* name, Helper const& helper, std::true_type){
        static_assert(std::is_polymorphic<W>::value &&
                      std::is_member_function_pointer<Function>::value &&
                      std::is_convertible<Function, decltype(helper.default_implementation())>::value,
                      "Virtual function default must be a derived class member");

        objects::add_to_namespace(
            *this, name,
            make_function(helper.default_implementation(), helper.policies(), helper.keywords())
        );
    }
    
    template<class Function, class Helper>
    void def_default(char const*, Helper const&, std::false_type) {}

    //
    // These two overloads discriminate between def() as applied to
    // regular functions and def() as applied to the result of
    // BOOST_PYTHON_FUNCTION_OVERLOADS(). The final argument is used to
    // discriminate.
    template<class Function, class Overloads>
    void def_maybe_overloads(char const* name, Function, Overloads const& overloads,
                             detail::overloads_base const*)
    {
        detail::define_with_defaults<detail::get_signature_t<Function>>(name, overloads, *this);
    }

    template<class Function, class A1>
    void def_maybe_overloads(char const* name, Function f, A1 const& a1,
                             ...)
    {
        def_impl(name, f, detail::make_def_helper(a1), &f);
    }
};

}} // namespace boost::python

#endif // CLASS_DWA200216_HPP
