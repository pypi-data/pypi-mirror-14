# cython: language_level=3

from ._fibointheap cimport *

import sys

cdef class FibonacciIntHeap:

    def __dealloc__(self):
        fiboTreeExit(&self._treedat)
        for i in range(self._arenacount):
            free(self._arenas[i])
        free(self._arenas)
                
    cdef void _realloc(self):
        cdef IntData**  arenas
        cdef IntData*   newarena
        cdef size_t i
        
        if self._arenacount==0:
            arenas = <IntData**>malloc(10 * sizeof(IntData*))
        elif self._arenacount % 10 == 0:
            arenas = <IntData**>realloc(<void*>self._arenas,
                                        (self._arenacount+10) * sizeof(IntData*))
        else:
            arenas = self._arenas
            
        if arenas==NULL:
            raise SystemError
     
        self._arenas=arenas
            
        newarena = <IntData*>malloc(sizeof(IntData) * self._chunksize)
    
        if newarena==NULL:
            raise SystemError

        arenas[self._arenacount]=newarena
        self._arenacount+=1
        
        for i in range(self._chunksize-1):
            (<IntData**>(newarena+i))[0]=newarena+i+1
            
        (<IntData**>(newarena+self._chunksize-1))[0]=NULL
        
        if self._arenacount>1:
            (<IntData**>(self._arenas[self._arenacount-1]+self._chunksize-1))[0]=newarena
            
        self._last = newarena
        
    cdef void _setNode(self,IntData* node,int32_t data,size_t priority):
        
        fiboTreeDel(&self._treedat,<FiboNode*>node)
        node.priority = priority 
        node.data=data
        fiboTreeAdd(&self._treedat,<FiboNode*>node)
        

    cpdef size_t push(self,int32_t data,size_t priority) except * :
        cdef IntData* d = self._last
        cdef object odata = PyInt_FromLong(data)
        
        assert odata not in self._nodes,'you cannot insert two times the same key'
                
        self._nodes[odata]=PyInt_FromSsize_t(<size_t>self._last)
        self._last= (<IntData**>self._last)[0]
        
        if self._last == NULL:
            self._realloc()
        
        d.priority = priority
        d.data     = data 
        
        fiboTreeAdd(&self._treedat, &d.node)
       
        self._size+=1
                        
        return priority
               
    cpdef tuple pop(self):
        cdef FiboNode *node 
        cdef IntData     *d
        cdef size_t   n
        
        assert self._size > 0,"You cannot pop from an empty heap"
        
        node = fiboTreeMin(&self._treedat)
        d = <IntData*>node
        data = d.data 
        fiboTreeDel(&self._treedat,node)
        self._size-=1
                       
        (<IntData**>d)[0]=self._last
        self._last = d
        
        del self._nodes[PyInt_FromLong(d.data)]
        
        return d.data,d.priority
         
    cpdef int32_t popInt(self):
        cdef FiboNode *node 
        cdef IntData     *d
        cdef size_t   n
        
        assert self._size > 0,"You cannot pop from an empty heap"
        
        node = fiboTreeMin(&self._treedat)
        d = <IntData*>node
        data = d.data 
        fiboTreeDel(&self._treedat,node)
        self._size-=1
                       
        (<IntData**>d)[0]=self._last
        self._last = d
        
        del self._nodes[PyInt_FromLong(d.data)]
                
        return d.data 

    def __len__(self):
        return self._size
    
    def __iter__(self):
        
        while(self._size > 0):
            yield self.popInt()
            
    cpdef size_t getPriority(self, int32_t key)  except *:
        cdef IntData *d
        
        d = <IntData*>PyInt_AsSsize_t(self._nodes[PyInt_FromLong(key)])
        return d.priority
    
    def __getitem__(self,key):
        return self.getPriority(key)

    cpdef size_t setPriority(self, int32_t key, size_t priority) except *:
        cdef IntData *d = <IntData*>PyInt_AsSsize_t(self._nodes[PyInt_FromLong(key)])
        self._setNode(d,key,priority)
        return priority
    
    def __setitem__(self,int32_t key, size_t priority):
        try:
            self.setPriority(key,priority)
        except KeyError:
            self.push(key,priority)
            
    def __contains__(self,int32_t key):
        cdef object k = PyInt_FromLong(key)
        return k in self._nodes
    
        
