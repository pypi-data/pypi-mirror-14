# cython: language_level=3

from cpython cimport *
from orgasm.fiboheap.fibo cimport *
from libc.stdlib cimport malloc,realloc,free
from cpython.int cimport PyInt_AsSsize_t
from cpython.int cimport PyInt_FromLong
from cpython.int cimport PyInt_FromSsize_t

cdef extern from "inttypes.h":
    ctypedef int int32_t  
    ctypedef int int64_t  

cdef struct IntData:
    FiboNode            node                    
    size_t              priority
    int32_t             data                      

cdef class FibonacciIntHeap:

    cdef FiboTree  _treedat
    cdef dict      _nodes
    cdef IntData** _arenas
    cdef size_t    _arenacount
    cdef IntData*  _last 
    cdef size_t    _chunksize
    cdef size_t    _size

    cdef void _realloc(self)
    cdef void _setNode(self,IntData* node,int32_t data,size_t priority)
    cpdef size_t push(self,int32_t data,size_t priority) except *
    cpdef tuple pop(self)
    cpdef int32_t popInt(self)
    cpdef size_t getPriority(self, int32_t key)   except *
    cpdef size_t setPriority(self, int32_t key,size_t priority)   except *


