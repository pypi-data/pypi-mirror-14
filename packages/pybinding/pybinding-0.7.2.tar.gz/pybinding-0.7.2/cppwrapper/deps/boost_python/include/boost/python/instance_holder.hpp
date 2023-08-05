// Copyright David Abrahams 2002.
// Distributed under the Boost Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.boost.org/LICENSE_1_0.txt)
#ifndef INSTANCE_HOLDER_DWA2002517_HPP
# define INSTANCE_HOLDER_DWA2002517_HPP

# include <boost/python/detail/prefix.hpp>
# include <boost/python/type_id.hpp>

namespace boost { namespace python { 

// Base class for all holders
struct BOOST_PYTHON_DECL instance_holder {
public:
    instance_holder() = default;
    virtual ~instance_holder() = default;

    instance_holder(instance_holder const&) = delete;
    instance_holder& operator=(instance_holder const&) = delete;
    
    // return the next holder in a chain
    instance_holder* next() const { return m_next; }

    // When the derived holder actually holds by [smart] pointer and
    // null_ptr_only is set, only report that the type is held when
    // the pointer is null.  This is needed for proper shared_ptr
    // support, to prevent holding shared_ptrs from being found when
    // converting from python so that we can use the conversion method
    // that always holds the Python object.
    virtual void* holds(type_info, bool null_ptr_only) = 0;

    void install(PyObject* inst) noexcept;

    // These functions should probably be located elsewhere.
    
    // Allocate storage for an object of the given size at the given
    // offset in the Python instance<> object if bytes are available
    // there. Otherwise allocate size bytes of heap memory.
    static void* allocate(PyObject*, std::size_t offset, std::size_t size);

    // Deallocate storage from the heap if it was not carved out of
    // the given Python object by allocate(), above.
    static void deallocate(PyObject*, void* storage) noexcept;

private:
    instance_holder* m_next = nullptr;
};

}} // namespace boost::python

#endif // INSTANCE_HOLDER_DWA2002517_HPP
