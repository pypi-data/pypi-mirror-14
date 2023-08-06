# cython: language_level=3

from cpython cimport *
from .fibo cimport *
from libc.stdlib  cimport malloc,realloc,free

cdef struct Data:
    FiboNode            node                    
    int                 priority
    PyObject*           data                      

cdef int cmpFunc (const_FiboNode_ptr_const node1, const_FiboNode_ptr_const node2)

cdef class FibonacciHeap:

    cdef FiboTree _treedat
    cdef Data*    _arena
    cdef size_t   _arenasize
    cdef size_t   _last 
    cdef size_t   _chunksize
    cdef size_t   _size

    cdef void _realloc(self)
    cpdef push(self,int priority,object data)
    cpdef tuple min(self)
    cpdef object minItem(self)
    cpdef tuple pop(self)
    cpdef object popItem(self)

