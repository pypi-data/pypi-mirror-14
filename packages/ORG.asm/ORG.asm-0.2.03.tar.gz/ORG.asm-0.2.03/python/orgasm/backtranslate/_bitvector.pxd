# cython: language_level=3

cdef extern from "inttypes.h":
    ctypedef int int32_t  
    ctypedef int int64_t  
    ctypedef unsigned int uint32_t
    ctypedef unsigned int uint64_t


cdef class BitVector:

    cdef size_t         _size
    cdef size_t         _wsize
    cdef size_t         _vcount
    cdef size_t         *_count
    cdef uint32_t       *_data

    cpdef size_t set(self, size_t v, size_t pos)
    cpdef size_t unset(self, size_t v, size_t pos)
    cpdef size_t get(self,size_t v)
    cpdef clear(self)
    cdef size_t* counter(self)
    
        

