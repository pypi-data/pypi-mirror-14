# cython: language_level=3

from ._asmbgraph cimport *


cdef int sign(int x):
    if x < 0:
        x=-1
    if x > 0:
        x=1
    return x

cdef class AsmbGraph(DiGraph):
    """
    AsmbGraph is a specialisation of the Graph class dedicated to manage
    assembling graph for the orgasm assembler. It mainly manage the junction
    between the forward and reverse node and the unified way to name strictly
    identical reads in the graph
    """
    
    def __init__(self, str name, Index readIndex):
        '''
        
        '''
        
        # Call the super class constructor
        DiGraph.__init__(self,name)
        
        self._readIndex=readIndex
        

    cpdef dict addNode(self,int node):
        cdef char[50] buffer
        cdef char* pbuffer=buffer+1
        cdef char* nbuffer=buffer
        cdef bytes pkey
        cdef bytes nkey
        cdef dict  node_attrs
        cdef int   id
        cdef size_t coverage
        cdef set    equiv
        assert node < INT32_MAX,'Node id must be less than %d' % INT32_MAX
        assert node >= INT32_MIN,'Node id must be greater or equal than %d' % INT32_MIN
        assert node != 0,'Node id cannot be zero'
        
            
        id,coverage,equiv = self._readIndex.getIds(node)
            
        if id==0:
            print("#####> %s %s %s" % (node,id,equiv))
            
        snprintf(pbuffer,49,b"%d",id)
        nbuffer[0]=b'-'
        pkey = pbuffer
        nkey = nbuffer
        
        if pkey not in self._nodes:
            e5pc = self._readIndex.getRead(id,0,1)
            e5pc = {b'A':b'T',b'C':b'G',b'G':b'C',b'T':b'A'}[e5pc]
            e3p = self._readIndex.getRead(id,self._readIndex.getReadSize()-1,1)
            
            self._nodes[pkey]=(set(),set())
            self._nodes[nkey]=(set(),set())
            node_attrs={"label" : pkey, 
                        'coverage':coverage, 
                        'reads':equiv,
                        'e5pc':e5pc,
                        'e3p':e3p}
            self._nodes_attrs[pkey]=node_attrs
            self._nodes_attrs[nkey]=node_attrs
        else:
            node_attrs=self._nodes_attrs[pkey]
            
        return node_attrs
            
    cpdef dict addEdge(self,int node1, int node2):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef char* pbuffer1=buffer1+1
        cdef char* nbuffer1=buffer1
        cdef char* pbuffer2=buffer2+1
        cdef char* nbuffer2=buffer2
        cdef int   id1
        cdef int   id2
        cdef bytes ikey1 
        cdef bytes okey1 
        cdef bytes ikey2 
        cdef bytes okey2 
        cdef tuple edg
        cdef dict edges_attrs
        cdef size_t coverage                            # @DuplicatedSignature
        cdef set    equiv                               # @DuplicatedSignature
        cdef int   d1
        cdef int   d2
        cdef int   tmp
        
        id1,coverage,equiv = self._readIndex.getIds(node1)
        d1 = 1 if node1 in equiv else -1

        id2,coverage,equiv = self._readIndex.getIds(node2)
        d2 = 1 if node2 in equiv else -1
                    

        snprintf(pbuffer1,49,b"%d",id1)
        nbuffer1[0]=b'-'
        
        snprintf(pbuffer2,49,b"%d",id2)
        nbuffer2[0]=b'-'
        
        if d1==1:
            okey1=pbuffer1
            ikey1=nbuffer1
            label2=self._nodes_attrs[okey1]['e5pc']
        else:
            okey1=nbuffer1
            ikey1=pbuffer1
            label2=self._nodes_attrs[okey1]['e3p']
            
        if d2==1:
            okey2=nbuffer2
            ikey2=pbuffer2
            label1=self._nodes_attrs[okey2]['e3p']
        else:
            okey2=pbuffer2
            ikey2=nbuffer2
            label1=self._nodes_attrs[okey2]['e5pc']
            
        
        edge = (okey1,ikey2)
        
        if edge not in self._edges_attrs:
            self._nodes[okey1][0].add(ikey2)
            self._nodes[ikey2][1].add(okey1) 
            edges_attrs1={'ext':label1 }
            self._edges_attrs[edge]=edges_attrs1
        else:
            edges_attrs1=self._edges_attrs[edge]

        edge = (okey2,ikey1)
        
        if edge not in self._edges_attrs:
            self._nodes[okey2][0].add(ikey1)
            self._nodes[ikey1][1].add(okey2) 
            edges_attrs2={'ext': label2}
            self._edges_attrs[edge]=edges_attrs2
        else:
            edges_attrs2=self._edges_attrs[edge]
        

        return {1:edges_attrs1,2:edges_attrs2}
    
    
    cpdef deleteEdge(self, int node1, int node2, int edge=-1):
        DiGraph.deleteEdge(self, node1 , node2, edge)
        DiGraph.deleteEdge(self, -node2, -node1, edge)
        
    cpdef deleteNode(self, int node):
        DiGraph.deleteNode(self, node)
        DiGraph.deleteNode(self, -node)

    cpdef dict getNodeAttr(self, int node):
        cdef int inode
        try:
            inode = self._readIndex.getIds(node)[0]
        except IndexError as e:
            inode = node
            
        return DiGraph.getNodeAttr(self, inode)
 


        