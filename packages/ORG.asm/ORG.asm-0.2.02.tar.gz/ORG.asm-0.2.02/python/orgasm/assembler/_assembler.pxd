from ._asmbgraph cimport  AsmbGraph
from orgasm.graph._graphmultiedge cimport DiGraphMultiEdge
from orgasm.indexer._orgasm cimport Index
    


cdef class Assembler:
    cdef AsmbGraph _graph
    cdef Index _index
    cdef int _overlap
    cdef set extensionPoints 
    cdef int _startread
    cdef int _finalread
    cdef list _seeds
    cdef dict _annotations

    cpdef tuple readType(self,ids)

cpdef dict buildstem(Assembler assembler,
               int first,
               int last,
               bytes sequence,
               list path,
               bint circle)


# cdef class Stem(dict):
#     cdef int   _first
#     cdef int   _last
#     cdef int   _length
#     cdef bytes _sequence
#     cdef list  _path
#     cdef bint  _palindrome
#     cdef str   _label
#     cdef int   _weight
#     cdef bint  _circle
#     cdef int   _stemid
#  
#     cdef bint isPalindrome(self)
#     cdef str buildLabel(self)
#     cdef int getWeight(self, Assembler graph)  except 0
 
cdef class CompactAssembling(DiGraphMultiEdge):
    cdef dict _paths 
    cdef dict _stemid
    cdef bint _stemidOk
    cdef Assembler _assembler
    
    cdef int getStemid(self, dict stem) except 0
    cdef void setStemid(self)
    cpdef dict addStem(self, dict stem)
    
    
   

cdef class StemIterator:
    cdef dict       edgeName
    cdef Assembler  _assembler
    cdef AsmbGraph  _graph

