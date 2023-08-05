#pragma once
#include <limits>
#include <stdexcept>

namespace boost { namespace python { namespace detail {

template<bool target_is_signed, bool source_is_signed>
struct less_than_helper {
    template<class Target, class Source>
    static bool check(Source x) {
        return x < std::numeric_limits<Target>::min();
    }
};

template<>
struct less_than_helper<true, false> {
    template<class Target, class Source>
    static bool check(Source) {
        return false;
    }
};

template<>
struct less_than_helper<false, true> {
    template<class Target, class Source>
    static bool check(Source x) {
        return x < 0;
    }
};

template<class Target, class Source>
bool is_negative_overflow(Source x) {
    return less_than_helper<
        std::numeric_limits<Target>::is_signed,
        std::numeric_limits<Source>::is_signed
    >::template check<Target>(x);
}

template<bool same_signedness, bool source_is_signed>
struct greater_than_helper {
    template<class Target, class Source>
    static bool check(Source x) {
        return x > std::numeric_limits<Target>::max();
    }
};

template<>
struct greater_than_helper<false, true> {
    template<class Target, class Source>
    static bool check(Source x) {
        return x >= 0 && static_cast<Source>(static_cast<Target>(x)) != x;
    }
};

template<>
struct greater_than_helper<false, false> {
    template<class Target, class Source>
    static bool check(Source x) {
        return static_cast<Source>(static_cast<Target>(x)) != x;
    }
};

template<class Target, class Source>
bool is_positive_overflow(Source x) {
    return greater_than_helper<
        std::numeric_limits<Source>::is_signed == std::numeric_limits<Target>::is_signed,
        std::numeric_limits<Source>::is_signed
    >::template check<Target>(x);
}

template<class Target, class Source>
inline Target check_overflow(Source source) {
    if (is_negative_overflow<Target>(source))
        throw std::overflow_error{"bad conversion: negative overflow"};
    else if(is_positive_overflow<Target>(source))
        throw std::overflow_error{"bad conversion: positive overflow"};
    return static_cast<Target>(source);
}

}}} // namespace boost::python::detail
