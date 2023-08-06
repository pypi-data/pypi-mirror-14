# cython: language_level=3

from ._fibointheap cimport *

cdef int cmpMinIntFunc(const_FiboNode_ptr_const node1, const_FiboNode_ptr_const node2)

cdef class FibonacciMinIntHeap(FibonacciIntHeap):


    cpdef tuple min(self)
    cpdef int32_t minInt(self)


