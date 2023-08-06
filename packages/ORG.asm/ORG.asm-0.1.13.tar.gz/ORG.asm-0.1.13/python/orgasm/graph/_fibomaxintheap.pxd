# cython: language_level=3

from ._fibointheap cimport *

cdef int cmpMaxIntFunc(const_FiboNode_ptr_const node1, const_FiboNode_ptr_const node2)

cdef class FibonacciMaxIntHeap(FibonacciIntHeap):


    cpdef tuple max(self)
    cpdef int32_t maxInt(self)


