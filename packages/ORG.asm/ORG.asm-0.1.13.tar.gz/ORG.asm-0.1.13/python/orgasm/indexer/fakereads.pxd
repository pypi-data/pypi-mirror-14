# cython: language_level=3

from cpython.dict cimport *
from cpython.int cimport PyInt_FromLong, PyInt_AsLong
from cpython.bytes cimport PyBytes_FromStringAndSize, PyBytes_GET_SIZE
from libc.stdio cimport snprintf
from orgasm.utils.dna cimport *

cdef extern from "inttypes.h":
    ctypedef int int32_t  
    ctypedef unsigned int uint32_t

cdef extern from "stdlib.h":      
    ctypedef unsigned int size_t  
    int32_t abs(int32_t i)
    
cdef extern from "math.h":
    double log10(double x)
    double ceil(double x)

cdef class FakeReads(dict):

    cdef dict   _reverse
    cdef dict   _keys
    cdef size_t _firstid
    cdef size_t _nextid
    cdef size_t _readsize
    
    cdef int _getid(self, bytes seq)
    cdef bint isFake(self, int32_t id)
    cpdef tuple getReadIds(self, bytes seq)
    cpdef tuple getIds(self, int32_t id)    
    cpdef bytes getRead(self, int32_t readid, int32_t begin, int32_t length)
    cpdef int len(self)
