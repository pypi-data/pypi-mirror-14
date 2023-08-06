# cython: language_level=3

from ._fiboheap cimport *
import sys

cdef int cmpFunc (const_FiboNode_ptr_const node1, const_FiboNode_ptr_const node2):
    cdef Data *data1 = <Data*> node1
    cdef Data *data2 = <Data*> node2

    return -1 if (data1.priority < data2.priority) else 1
 

cdef class FibonacciHeap:

    def __init__(self,object data=None,size_t chunksize=1000):
        
        cdef size_t i
          
        if (fiboTreeInit (&self._treedat, cmpFunc) != 0):
            raise SystemError
        
        self._last=0
        self._size=0
        self._chunksize=chunksize
        self._arenasize=chunksize
        self._arena = <Data*> malloc(sizeof(Data) * chunksize)
        
        for i in range(chunksize):
            (<size_t*>(self._arena+i))[0]=i+1
        
        if self._arena==NULL:
            raise SystemError
        
        if data is not None:
            for d in data:
                try:
                    priority = d[0]
                    d = d[1:]
                except :
                    priority = d 
                    d = None
                    
                self.push(priority,d)
                
    def __dealloc__(self):
        fiboTreeExit(&self._treedat)
        free(self._arena)
                
    cdef void _realloc(self):
        cdef size_t newsize = self._arenasize+self._chunksize
        cdef Data*  newarena= <Data*>realloc(<void*>self._arena,sizeof(Data) * newsize)
        cdef size_t i
        
        if newarena==NULL:
            raise SystemError

        for i in range(self._arenasize,newsize):
            (<size_t*>(self._arena+i))[0]=i+1
            

        self._arenasize=newsize
        self._arena=newarena
                

    cpdef push(self,int priority,object data):
        cdef Data* d = self._arena + self._last
                
        self._last= (<size_t*> (self._arena+self._last))[0]
        
        if self._last == self._arenasize:
            self._realloc()
        
        d.priority = priority
        d.data     = <PyObject*>data 
        Py_INCREF(data)
        
        fiboTreeAdd(&self._treedat, &d.node)
        
        self._size+=1
        
    cpdef tuple min(self):
        cdef FiboNode *node 
        cdef Data     *d
        cdef object   data   
        
        node = fiboTreeMin(&self._treedat)
        d = <Data*>node
        data = <object> d.data 
             
        return d.priority,data
    
    cpdef object minItem(self):
        cdef FiboNode *node 
        cdef Data     *d
        cdef object   data   
        
        node = fiboTreeMin(&self._treedat)
        d = <Data*>node
        data = <object> d.data 
             
        return data
    
        
    cpdef tuple pop(self):
        cdef FiboNode *node 
        cdef Data     *d
        cdef object   data   
        cdef size_t   n
        
        assert self._size > 0,"You cannot pop from an empty heap"
        
        node = fiboTreeMin(&self._treedat)
        d = <Data*>node
        data = <object> d.data 
        fiboTreeDel(&self._treedat,node)
        Py_DECREF(data)
        self._size-=1
        
        n = d - self._arena
               
        (<size_t*>d)[0]=self._last
        self._last = n
        
        return d.priority,data
         
    cpdef object popItem(self):
        cdef FiboNode *node 
        cdef Data     *d
        cdef object   data   
        cdef size_t   n
        
        assert self._size > 0,"You cannot pop from an empty heap"
        
        node = fiboTreeMin(&self._treedat)
        d = <Data*>node
        data = <object> d.data 
        fiboTreeDel(&self._treedat,node)
        Py_DECREF(data)
        self._size-=1
        
        n = d - self._arena
               
        (<size_t*>d)[0]=self._last
        self._last = n
        
        return data

    def __len__(self):
        return self._size
        
    def __iter__(self):
        
        while(self._size > 0):
            yield self.popItem()
        
