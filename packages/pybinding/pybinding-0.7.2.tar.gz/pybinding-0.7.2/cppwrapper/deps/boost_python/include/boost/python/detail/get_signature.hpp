#ifndef BOOST_PYTHON_FN_CC
#error Do not include this file
#else

// 'Return (*)(Args...)' is the same function as 'Return (__cdecl *)(Args...)'
// -> we don't define it twice
#if !defined(BOOST_PYTHON_FN_CC_IS_CDECL)

// Non-member functions
template<class Return, class _, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC *)(Args...), _> {
    using type = type_list<Return, Args...>;
};

#endif

// Member functions
template<class Return, class Class, class Target, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC Class::*)(Args...), Target> {
    using type = type_list<Return, most_derived_t<Target, Class>&, Args...>;
};

template<class Return, class Class, class Target, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC Class::*)(Args...) const, Target> {
    using type = type_list<Return, most_derived_t<Target, Class>&, Args...>;
};

template<class Return, class Class, class Target, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC Class::*)(Args...) volatile, Target> {
    using type = type_list<Return, most_derived_t<Target, Class>&, Args...>;
};

template<class Return, class Class, class Target, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC Class::*)(Args...) const volatile, Target> {
    using type = type_list<Return, most_derived_t<Target, Class>&, Args...>;
};

// Functor and lambda
template<class Return, class Class, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC Class::*)(Args...), int> {
    using type = type_list<Return, Args...>;
};

template<class Return, class Class, class... Args>
struct get_signature<Return(BOOST_PYTHON_FN_CC Class::*)(Args...) const, int> {
    using type = type_list<Return, Args...>;
};

#endif // BOOST_PYTHON_FN_CC
