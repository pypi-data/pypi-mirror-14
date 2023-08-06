# cython: language_level=3

from ._graphmultiedge cimport *
from cpython.list cimport PyList_Size
from builtins import isinstance

cdef class DiGraphMultiEdge(DiGraph):

    cpdef dict addEdge(self,int node1, int node2):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edge
        cdef list eattr
        cdef int eid
        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
        
        edge = (key1,key2)
        
        if edge not in self._edges_attrs:
            self.addNode(node1)
            self.addNode(node2)
        
            self._nodes[key1][0].add(key2)
            self._nodes[key2][1].add(key1)

            self._edges_attrs[edge]=[]
            
        eattr = self._edges_attrs[edge]
        eattr.append({})
        #eid = PyList_Size(eattr)-1
            
        self._edgecount+=1
        
        return eattr[-1]
            
    cpdef dict getEdgeAttr(self, int node1, int node2,int edge=-1):
 
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edgek
        cdef list attr
        cdef dict rep
        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
   
        edgek = (key1,key2)
        
        attr = self._edges_attrs[edgek]
        
        return attr[edge]
    
    cpdef int edgeCount(self):
        return self._edgecount
    
    cpdef deleteEdge(self, int node1, int node2, int edge=-1):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edgek
        cdef list edgel

        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
   
        edgek = (key1,key2)
        
        edgel = self._edges_attrs[edgek]
        
        del edgel[edge]
        self._edgecount-=1
        
        if not edgel:
            del self._edges_attrs[edgek]
            
            self._nodes[key1][0].remove(key2)
            self._nodes[key2][1].remove(key1)

    cpdef deleteAllEdges(self, int node1, int node2):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edgek
        cdef list edgel
        cdef int nedge

        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
   
        edgek = (key1,key2)
        nedge = len(self._edges_attrs[edgek])
        
        del self._edges_attrs[edgek]
        self._nodes[key1][0].remove(key2)
        self._nodes[key2][1].remove(key1)
       
        self._edgecount-=nedge
        
    cpdef deleteNode(self, int node):
        cdef char[50] buffer
        cdef bytes key
        cdef dict attr
        cdef int node2
        cdef list edges
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        del self._nodes_attrs[key]
        
        edges = list(self.neighbourIterator(node))
        for node2 in edges:
            self.deleteAllEdges(node,node2)
            
        edges = list(self.parentIterator(node))
        for node2 in edges:
            self.deleteAllEdges(node2,node)
            
        del self._nodes[key]


    def edgeIterator(self,nodePredicate=None, edgePredicate=None):
        cdef tuple edge
        cdef bytes key1
        cdef bytes key2
        cdef int   node1
        cdef int   node2
        cdef int   edgei
        cdef int  edgel
        
        for edge in self._edges_attrs:
            key1 = edge[0]
            key2 = edge[1]
            
            node1 = atol(key1)
            node2 = atol(key2)
            
            if nodePredicate is None or (nodePredicate(node1) and nodePredicate(node2)):
                edgel = len(self._edges_attrs[(key1,key2)])
                for edgei in range(edgel):
                    edge=(node1,node2,edgei)
                    if edgePredicate is None or edgePredicate(edge):
                        yield edge
                    
                
    def parentIterator(self,int node,nodePredicate=None, edgePredicate=None):
        cdef char[50] buffer
        cdef bytes key1
        cdef bytes key2
        cdef set neighbours
        cdef int n 
        cdef int edgel
        cdef int edgei
        cdef bint edgeok
        
        snprintf(buffer,50,b"%d",node)
        key1 = buffer
        
        neighbours = self._nodes[key1][1]
        
        for key2 in neighbours:
            n = atol(key2)
            if nodePredicate is None or nodePredicate(n):
                edgel = len(self._edges_attrs[(key2,key1)])
                edgeok = True
                if edgePredicate is not None :
                    for edgei in range(edgel):
                        edgeok=edgeok and edgePredicate((n,node,edgei))
                if edgePredicate is None or edgeok:
                    yield n
                
    def neighbourIterator(self,int node,nodePredicate=None, edgePredicate=None):
        cdef char[50] buffer
        cdef bytes key1
        cdef bytes key2
        cdef set neighbours
        cdef int n 
        cdef int edgel
        cdef int edgei
        cdef bint edgeok
        
        snprintf(buffer,50,b"%d",node)
        key1 = buffer
        
        neighbours = self._nodes[key1][0]
        
        for key2 in neighbours:
            n = atol(key2)
            if nodePredicate is None or nodePredicate(n):
                edgel = len(self._edges_attrs[(key1,key2)])
                edgeok = True
                if edgePredicate is not None :
                    for edgei in range(edgel):
                        edgeok=edgeok and edgePredicate((node,n,edgei))
                if edgePredicate is None or edgeok:
                    yield n
                    

