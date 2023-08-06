# cython: language_level=3

from ._fibominintheap cimport *
from ._fibomaxintheap cimport *

from libc.stdio cimport snprintf
from libc.stdlib cimport atol

cdef extern from "inttypes.h":
    cdef enum:
        INT32_MAX
        INT32_MIN
        
cdef class NodeIterator:

    cdef object   _nodepredicate
    cdef object   _nodeiterator
    cdef set      _exclude
    cdef DiGraph  _graph  

    cpdef add(self,int node)
    cpdef remove(self, int node)

cdef class DiGraph:

    cdef dict _nodes
    cdef dict _edges_attrs
    cdef dict _nodes_attrs
    cdef str _name
    
    cpdef dict addNode(self,int node)
    cpdef dict addEdge(self,int node1, int node2)
    cpdef bint hasEdge(self, int node1, int node2)  
    cpdef dict getEdgeAttr(self, int node1, int node2,int edge=?)
    cpdef dict getNodeAttr(self, int node)
    cpdef int nodeCount(self)
    cpdef int edgeCount(self)
    cpdef str dot(self,nodePredicate=?, edgePredicate=?)
    cpdef str gml(self,nodePredicate=?, edgePredicate=?)
    cpdef deleteEdge(self, int node1, int node2,int edge=?)
    cpdef deleteNode(self, int node)
    cpdef DiGraph subgraph(self,str name, nodes)
    cpdef set connectedComponent(self,int node, nodePredicate=?, edgePredicate=?)
    