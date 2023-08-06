# cython: language_level=3

from ._fibomaxintheap cimport *

import sys

cdef int cmpMaxIntFunc(const_FiboNode_ptr_const node1, const_FiboNode_ptr_const node2):
    cdef IntData *data1 = <IntData*> node1
    cdef IntData *data2 = <IntData*> node2

    return -1 if (data1.priority > data2.priority) else 1


cdef class FibonacciMaxIntHeap(FibonacciIntHeap):

    def __init__(self,object data=None,size_t chunksize=1000):
        
        cdef size_t i
        cdef size_t priority 
        cdef int32_t di
          
        if fiboTreeInit(&self._treedat, cmpMaxIntFunc) != 0:
            raise SystemError
        
        self._last=NULL
        self._size=0
        self._chunksize=chunksize
        self._arenacount=0
        self._realloc()
        self._nodes = {}
               
        if data is not None:
            for d in data:
                try:
                    priority = d[0]
                    di = d[1]
                except :
                    priority = d
                    di = priority
                    
                self.push(priority,di)
                
        
    cpdef tuple max(self):
        cdef FiboNode *node 
        cdef IntData     *d
        
        assert self._size > 0,"Heap is empty"

        node = fiboTreeMin(&self._treedat)
        d = <IntData*>node
             
        return d.data,d.priority
    
    cpdef int32_t maxInt(self):
        cdef FiboNode *node 
        cdef IntData     *d
        
        assert self._size > 0,"Heap is empty"

        node = fiboTreeMin(&self._treedat)
        d = <IntData*>node
             
        return d.data
    
        
        
