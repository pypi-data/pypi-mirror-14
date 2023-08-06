# cython: language_level=3

from orgasm.graph._graph cimport *
from orgasm.indexer._orgasm cimport *

cdef class AsmbGraph(DiGraph):
    cdef Index _readIndex
    
    cpdef dict addNode(self,int node)
    cpdef dict addEdge(self,int node1, int node2)
    cpdef dict getNodeAttr(self, int node)

