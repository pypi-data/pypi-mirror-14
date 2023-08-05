// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef KEYWORDS_DWA2002323_HPP
# define KEYWORDS_DWA2002323_HPP

# include <boost/python/detail/prefix.hpp>

# include <boost/python/args_fwd.hpp>
# include <boost/python/object_core.hpp>

# include <algorithm>

namespace boost { namespace python {

using arg = detail::keywords<1>;
using kerword = detail::keywords<1>;

namespace detail
{
  template <std::size_t nkeywords>
  struct keywords_base {
      static constexpr auto size = nkeywords;
      keyword elements[nkeywords];

      // This is needed on some compilers which assume the template below is also a move ctor
      keywords_base(keywords_base const&) = default;
      keywords_base(keywords_base&&) = default;
      keywords_base& operator=(keywords_base const&) = default;
      keywords_base& operator=(keywords_base&&) = default;

      template<typename... Ts>
      explicit keywords_base(Ts&&... args) : elements{std::forward<Ts>(args)...} {}

      keyword_range range() const {
          return keyword_range(elements, elements + nkeywords);
      }

      keywords<nkeywords+1>
      operator,(python::arg const &k) const;

      keywords<nkeywords + 1>
      operator,(char const *name) const;
  };
  
  template <std::size_t nkeywords>
  struct keywords : keywords_base<nkeywords> {
      using keywords_base<nkeywords>::keywords_base;
  };

  template <>
  struct keywords<1> : keywords_base<1> {
	  explicit keywords(char const* name) : keywords_base<1>(name) {}
	  explicit keywords(keyword kw) : keywords_base<1>(kw) {}

      template <class T>
      keywords<1>& operator=(T value) {
          elements[0].default_value = handle<>(python::borrowed(object(value).ptr()));
          return *this;
      }
    
      operator detail::keyword const&() const {
          return elements[0];
      }
  };

  template <std::size_t nkeywords>
  inline keywords<nkeywords+1> keywords_base<nkeywords>::operator,(python::arg const& k) const {
      python::detail::keywords<nkeywords+1> res;
      std::copy(elements, elements+nkeywords, res.elements);
      res.elements[nkeywords] = k.elements[0];
      return res;
  }

  template <std::size_t nkeywords>
  inline keywords<nkeywords + 1> keywords_base<nkeywords>::operator,(char const* name) const {
      return this->operator,(python::arg(name));
  }

  template<typename T>
  struct is_keywords : std::false_type {};

  template<std::size_t nkeywords>
  struct is_keywords<keywords<nkeywords>> : std::true_type {};
}

inline namespace literals {
    inline kerword operator"" _kw(char const* str, std::size_t) {
        return kerword{str};
    }
}

template<typename... Ts, int N = sizeof...(Ts)>
inline detail::keywords<N> args(Ts&&... names) {
    return detail::keywords<N>{detail::keyword(std::forward<Ts>(names))...};
}

}} // namespace boost::python

# endif // KEYWORDS_DWA2002323_HPP
