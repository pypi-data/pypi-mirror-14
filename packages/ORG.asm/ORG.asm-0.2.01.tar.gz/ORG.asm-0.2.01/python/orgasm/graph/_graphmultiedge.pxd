# cython: language_level=3

from ._graph cimport *

cdef class DiGraphMultiEdge(DiGraph):

    cdef int _edgecount

    cpdef deleteAllEdges(self, int node1, int node2)
    
