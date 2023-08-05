// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef EXCEPTION_HANDLER_DWA2002810_HPP
# define EXCEPTION_HANDLER_DWA2002810_HPP

# include <boost/python/detail/config.hpp>
# include <functional>
# include <memory>

namespace boost { namespace python { namespace detail {

struct BOOST_PYTHON_DECL_FORWARD exception_handler;

using handler_function = std::function<
    bool(exception_handler const&, std::function<void()> const&)
>;

struct BOOST_PYTHON_DECL exception_handler
{
    static std::unique_ptr<exception_handler> chain;

    static void add(handler_function const& f) {
        auto& new_tail = chain ? tail->m_next : chain;
        new_tail.reset(new exception_handler(f));
        tail = new_tail.get();
    };

    bool handle(std::function<void()> const& f) const {
        return m_impl(*this, f);
    }

    bool operator()(std::function<void()> const& f) const {
        if (m_next)
            return m_next->handle(f);
        f();
        return false;
    }

private:
    explicit exception_handler(handler_function const& impl) : m_impl(impl) {}

    static exception_handler* tail;

    handler_function m_impl;
    std::unique_ptr<exception_handler> m_next;
};

}}} // namespace boost::python::detail

#endif // EXCEPTION_HANDLER_DWA2002810_HPP
