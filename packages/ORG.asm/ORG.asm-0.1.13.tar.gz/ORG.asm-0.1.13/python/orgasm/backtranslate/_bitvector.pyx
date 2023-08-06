# cython: language_level=3

from ._bitvector cimport *

from libc.stdlib  cimport malloc,realloc,free
cdef extern from "strings.h":
    void bzero(void *s, size_t n)


        
cdef class BitVector:
    
    def __init__(self, size_t vcount, size_t size):
        cdef size_t     wsize = (size >> 5) + (1 if (size & 31) else 0)
        
        self._size=wsize * vcount * sizeof(uint32_t)
        self._wsize=wsize
        self._vcount=vcount
        
        self._count = <size_t*>malloc(sizeof(size_t) * vcount)
        self._data  = <uint32_t*>malloc(self._size)
        
        self.clear()
 
    def __dealloc__(self):
        if self._count != NULL:
            free(self._count)
        if self._data != NULL:
            free(self._data)
            
        
    cpdef size_t set(self, size_t v,size_t pos):
        cdef size_t bit = 1 << (pos & 31)
        cdef size_t addr= (pos >> 5) + v * self._wsize
        
        if (self._data[addr] & bit)==0:
            self._data[addr] |= bit
            self._count[v]+=1
            
        return self._count[v]
            
    
    cpdef size_t unset(self, size_t v,size_t pos):
        cdef size_t bit = 1 << (pos & 31)
        cdef size_t addr= (pos >> 5) + v * self._wsize
        
        if (self._data[addr] & bit)>0:
            self._data[addr] &= ~bit
            self._count[v]-=1
            
        return self._count[v]
    
    cpdef size_t get(self, size_t v):
        return self._count[v]

    cpdef clear(self):
        bzero(self._data,self._size)
        bzero(self._count,self._vcount * sizeof(size_t))
        
    cdef size_t* counter(self):
        return self._count
        
    def __getitem__(self, size_t v):
        return self.get(v)
    
    def __len__(self):
        return self._vcount
    
        

        