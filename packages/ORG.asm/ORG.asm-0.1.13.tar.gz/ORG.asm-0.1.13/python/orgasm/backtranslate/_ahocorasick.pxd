# cython: language_level=3

from cpython.ref cimport PyObject,Py_XDECREF

#
# C API to Bytes object
#

from cpython.bytes  cimport PyBytes_Size, PyBytes_FromStringAndSize

# We explicitly want access to the raw version of the PyBytes_AS_STRING macro
# that can be called with a PyObject* 
cdef extern from "Python.h":
    char* PyBytes_AS_STRING(PyObject* obj)

#
# C API to Dict object
#

from cpython.dict  cimport PyDict_New,PyDict_GetItemString,PyDict_SetItemString
from cpython.dict  cimport PyDict_Next,PyDict_SetItem,PyDict_GetItem,PyDict_Size

#
# C API to List object
#

from cpython.list  cimport PyList_GET_SIZE, PyList_Append

#
# C API to Tuple object
#

from cpython.tuple  cimport PyTuple_GET_ITEM

#
# C API to int object
#

from cpython.int  cimport PyInt_AsSsize_t,PyInt_FromLong

#
# C API to the libc
#

from libc.stdlib  cimport malloc,realloc,free
from libc.math cimport log
from libc.string cimport strlen,memcpy

cdef extern from "strings.h":
    void bzero(void *s, size_t n)

from orgasm.graph._graphmultiedge cimport DiGraphMultiEdge
from orgasm.indexer._orgasm cimport Index

cdef dict listCodons2Dict(tuple codons)
cpdef dict bindCodons(dict codon1, dict codon2)
cpdef dict codon(char aa, bint direct=?)

cdef struct protmatch:
    int        protid
    int        position
    protmatch* next

cdef struct dnastate:
#    dnastate*  error
    protmatch* match
    dnastate*  a 
    dnastate*  c 
    dnastate*  t 
    dnastate*  g 
   
cdef extern from "inttypes.h":
    ctypedef int int32_t  
    ctypedef int int64_t  
    ctypedef unsigned int uint32_t
    ctypedef unsigned int uint64_t

cdef extern from "orgasm.h":
    uint32_t expanded8bitsnuc[]
 

cdef class AhoCorasick:

    cdef dnastate *_states
    cdef size_t   _statesize
    cdef size_t   _statecount
    
    cdef protmatch *_matches 
    cdef size_t    _matchsize
    cdef size_t    _matchcount
    
    # the automata has been finalized
    cdef bint      _finalized
    
    cdef size_t    _step
    cdef size_t    _depth
    cdef int       _maxseqid
    cdef size_t    _maxpos
    
    cdef dict      _seqid
    cdef dict      _rseqid
    

    cdef dnastate *getNextState(self,dnastate *base, int letter)
    cdef protmatch* setAsTerminal(self, dnastate* base, int protid, int position)
    cdef dnastate* simpleMatch(self,char* cword, size_t lword)
    cdef dnastate* longestSuffix(self,char* cword, size_t lword)
    cdef setErrorLink(self)
    cpdef finalize(self)
    cdef int addCWord(self,char* cword, size_t lword, int protid, int position)
    cdef int addAutomata(self,dict automata,int protid, int position)
    cpdef dict match(self,bytes sequence)    
    cpdef DiGraphMultiEdge asGraph(self)
    
cdef class ProtAhoCorasick(AhoCorasick):

    cpdef int addSequence(self,bytes sequence, object seqid=?, size_t kup=?)
    cpdef scanIndex(self,Index seqindex,int minmatch=?, int maxmatch=?, int covmin=?, bint progress=?)

cdef class NucAhoCorasick(AhoCorasick):

    cpdef int addSequence(self,bytes sequence, object seqid=?, size_t kup=?)
    cpdef scanIndex(self,Index seqindex,int minmatch=?, int maxmatch=?, int covmin=?, bint progress=?)

 
 