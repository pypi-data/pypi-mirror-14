from .fakereads cimport *
import traceback

cdef class FakeReads(dict):

    def __init__(self,size_t initid,size_t readsize=0):
        
        self._firstid = initid
        self._nextid  = initid
        self._readsize = readsize
        
        self._reverse = {}
        self._keys = {}
            
    cdef bint isFake(self, int32_t id):
        cdef bint rep =  abs(id) >= self._firstid and abs(id) < self._nextid
        return rep
    
    cdef int _getid(self, bytes seq):
        cdef bytes cseq
        cdef object oid
        cdef char[50] buffer
        cdef char* pbuffer=buffer+1
        cdef char* nbuffer=buffer
        cdef int id
        
        seq = seq.upper()
        
        oid = self.get(seq,None)

        if  oid is None:
            
            assert PyBytes_GET_SIZE(seq)==self._readsize
            
            #print 'Create a new fake sequence'
            #traceback.print_stack()
            
            id = self._nextid
            self._nextid+=1
            
            self[seq]=PyInt_FromLong(id)
            
            cseq = reverseComplement(seq)
            self[cseq]=PyInt_FromLong(-id)
            
            snprintf(pbuffer,49,b"%d",id)
            nbuffer[0]=b'-'
            self._reverse[pbuffer]=seq
            self._reverse[nbuffer]=cseq
        else:
            id = PyInt_AsLong(oid)
            
        return id
            
            
    cpdef tuple getReadIds(self, bytes seq):
        cdef int id = self._getid(seq)
    
        return (id,0,set([id]))

    cpdef tuple getIds(self, int32_t id):
        assert self.isFake(id)
        return (abs(id),0,set([abs(id)]))
    
    cpdef bytes getRead(self, int32_t readid, int32_t begin, int32_t length):
        cdef char[50] buffer
        cdef int id
        cdef bytes sequence
        cdef char* pseq

        assert self.isFake(readid)

        snprintf(buffer,50,b"%d",readid)
        sequence = self._reverse[buffer]
        pseq = <char*>sequence + begin 
        return PyBytes_FromStringAndSize(pseq,length)
     
    cpdef int len(self):
        return PyDict_Size(self)
        
    property firstid:

        "A doc string can go here."

        def __get__(self):
            return self._firstid

    property lastid:

        "A doc string can go here."

        def __get__(self):
            return self._nextid

            
            