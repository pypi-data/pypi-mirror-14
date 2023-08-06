# cython: language_level=3

from cpython.function cimport PyFunction_Check

from ._graph cimport *

cdef str formatDict(dict keys, bint intfloat=False, 
                      str sep0="[", str sep1="]", 
                      str sep2="=", str sep3=" ", 
                      str sep4="[", sep5="]"):
    cdef str key
    cdef list output=[]
    
    for key,val in keys.iteritems():
        if isinstance(val, dict):
            output.append('%s%s%s%s%s%s%s' % (key,sep2,sep4, sep3,formatDict(val, intfloat, sep0, sep1, sep2, sep3, sep4, sep5),sep3,sep5))
        elif isinstance(val, bytes):
            output.append('%s%s"%s"' % (key,sep2,val.decode('ascii')))
        elif isinstance(val, bool):
            output.append('%s%s"%s"' % (key,sep2,val))
        elif intfloat and (isinstance(val, int) or isinstance(val, float)):
            output.append('%s%s%s' % (key,sep2,val))
        else:
            output.append('%s%s"%s"' % (key,sep2,val))
    
    return str("%s%s%s" % (sep0, sep3.join(output), sep1))


cdef class NodeIterator:

    def __init__(self,DiGraph graph, object predicate=None):
        
    #    if predicate is not None and not PyFunction_Check(predicate):
    #        raise TypeError,"predicate must be a function or None"
        
        self._nodepredicate = predicate
        self._graph = graph 
        self._exclude = set()
        self._nodeiterator = iter(graph._nodes)
        
    cpdef add(self,int node):
        cdef char[50] buffer
        cdef bytes key                          # @DuplicatedSignature
        
        snprintf(buffer,50,b"%d",node)
        key = buffer

        self._exclude.add(key)
        
    cpdef remove(self, int node):
        cdef char[50] buffer                    # @DuplicatedSignature
        cdef bytes key                          # @DuplicatedSignature
        
        snprintf(buffer,50,b"%d",node)
        key = buffer

        self.exclude.remove(key)
        
                
    def __next__(self):
        cdef bytes key
        cdef int node
        cdef bint ok
        
        
        ok =False
        
        while(not ok):
            key = next(self._nodeiterator)
            node = atol(key)
            ok = (self._nodepredicate is None or self._nodepredicate(node)) \
                   and key not in self._exclude
                
        return node
    
    def __ior__(self,others):
        cdef int i
        
        for i in others:
            i=i+0
            self.add(i)
            
        return self

    def __iter__(self):
        return self
    
    

cdef class DiGraph:

    def __init__(self,str name):
        self._nodes={}
        self._edges_attrs={}
        self._nodes_attrs={}
        self._name=name 
        
    def __contains__(self,int node):
        cdef char[50] buffer
        cdef bytes key
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        return key in self._nodes
    
    cpdef dict addNode(self,int node):
        cdef char[50] buffer
        cdef bytes key
        cdef dict node_attrs
        
        assert node < INT32_MAX,'Node id must be less than %d' % INT32_MAX
        assert node >= INT32_MIN,'Node id must be greater or equal than %d' % INT32_MIN
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        if key not in self._nodes:
            self._nodes[key]=(set(),set())
            node_attrs={}
            self._nodes_attrs[key]=node_attrs
        else:
            node_attrs=self._nodes_attrs[key]
            
        return node_attrs
            
    cpdef dict addEdge(self,int node1, int node2):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edg
        cdef dict edges_attrs
        
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

            edges_attrs={}
            self._edges_attrs[edge]=edges_attrs
        else:
            edges_attrs=self._edges_attrs[edge]
            
        return edges_attrs
            
    cpdef bint hasEdge(self, int node1, int node2):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edgek
        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
   
        edgek = (key1,key2)

        return edgek in self._edges_attrs
    
    cpdef dict getEdgeAttr(self, int node1, int node2,int edge=-1):
 
        cdef char[50] buffer1           # @DuplicatedSignature
        cdef char[50] buffer2           # @DuplicatedSignature
        cdef bytes key1                 # @DuplicatedSignature
        cdef bytes key2                 # @DuplicatedSignature
        cdef tuple edgek                # @DuplicatedSignature
        cdef dict attr
        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
   
        edgek = (key1,key2)
        
        attr = self._edges_attrs[edgek]
        
        return attr 
    
    cpdef dict getNodeAttr(self, int node):
        cdef char[50] buffer        # @DuplicatedSignature
        cdef bytes key              # @DuplicatedSignature
        cdef dict attr              # @DuplicatedSignature
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        attr = self._nodes_attrs[key]
        
        return attr 

    cpdef int nodeCount(self):
        return len(self._nodes)
    
    cpdef int edgeCount(self):
        return len(self._edges_attrs)

    cpdef str gml(self,nodePredicate=None, edgePredicate=None):
        cdef str gml
        cdef int node1
        cdef int node2
        cdef int edge
        cdef list lines=[]
        cdef str line
       # cdef dict attr 
        

        for node1 in self.nodeIterator(nodePredicate):
            lines.append('node [\n')
            line = "id %10d\n" % node1 
            lines.append(line)
            attr = self.getNodeAttr(node1)
            
            if attr:
                line = formatDict(attr, True, '', '', '\t\t', '\n')
                lines.append(line)

            lines.append(']')
            
        for node1,node2,edge in self.edgeIterator(nodePredicate,edgePredicate):
            lines.append('edge [\n')
            lines.append('source %d\n'%node1)
            lines.append('target %d\n'%node2)
 
 
            attr = self.getEdgeAttr(node1,node2,edge)
            assert isinstance(attr, dict)
            if attr:
                line = formatDict(attr, True, '', '', '\t\t', '\n')
            lines.append(line)
            lines.append(']')
        
        gml = "\n\t".join(lines)
        gml = 'Creator "%s"\nVersion "0.0"\ngraph [\n\tdirected\t1\n\tname\t"%s"\n%s\n]' % (__name__, self._name,gml)
        return gml

    
    cpdef str dot(self,nodePredicate=None, edgePredicate=None):
        cdef str dot
        cdef int node1              # @DuplicatedSignature
        cdef int node2              # @DuplicatedSignature
        cdef int edge               # @DuplicatedSignature
        cdef list lines=[]          # @DuplicatedSignature
        cdef str line             # @DuplicatedSignature
        cdef dict attr              # @DuplicatedSignature
        
        for node1 in self.nodeIterator(nodePredicate):
            attr = self.getNodeAttr(node1)
            if attr:
                line = "   %10d %s" % (node1,formatDict(attr))
            else:
                line = "   %10d" % node1 
            lines.append(line)
            
        for node1,node2,edge in self.edgeIterator(nodePredicate,edgePredicate):
            attr = self.getEdgeAttr(node1,node2,edge)
            if attr:
                line = "   %10d -> %10d %s" % (node1,node2,formatDict(attr))
            else:
                line = "   %10d -> %10d" % (node1,node2)
            lines.append(line)
        
        dot = "\n".join(lines)
        dot = "digraph %s {\n%s\n}" % (self._name,dot)
        
        return dot

    cpdef deleteEdge(self, int node1, int node2, int edge=-1):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edgek

        
        snprintf(buffer1,50,b"%d",node1)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",node2)
        key2 = buffer2
   
        edgek = (key1,key2)
        
        del self._edges_attrs[edgek]
        
        self._nodes[key1][0].remove(key2)
        self._nodes[key2][1].remove(key1)
        
    cpdef deleteNode(self, int node):
        cdef char[50] buffer  # @DuplicatedSignature
        cdef bytes key  # @DuplicatedSignature
        cdef dict attr  # @DuplicatedSignature
        cdef int node2  # @DuplicatedSignature
        cdef list edges
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        edges = list(self.neighbourIterator(node))
        for node2 in edges:
            self.deleteEdge(node,node2)
            
        edges = list(self.parentIterator(node))
        for node2 in edges:
            self.deleteEdge(node2,node)
            
        del self._nodes[key]
        del self._nodes_attrs[key]
        
            
    cpdef DiGraph subgraph(self,str name, nodes):
        cdef DiGraph graph
        cdef set nodeset = set()
        cdef int node
        cdef int node2
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1
        cdef bytes key2
        cdef tuple edge
        cdef set n0
        cdef set n1
        
        graph = self.__class__(name)
        
        for node in nodes:
            snprintf(buffer1,50,b"%d",node)
            key1 = buffer1
            nodeset.add(key1)
            
        for key1 in nodeset:
            n0 = self._nodes[key1][0]
            n1 = self._nodes[key1][1]
            
            graph._nodes[key1] = (n0 & nodeset, n1 & nodeset)
            graph._nodes_attrs[key1] = self._nodes_attrs[key1]
            
            for key2 in graph._nodes[key1][0]:
                edge=(key1,key2)                
                graph._edges_attrs[edge]=self._edges_attrs[edge]
        
        return graph
    
    cpdef set connectedComponent(self,int node, nodePredicate=None, edgePredicate=None):
        cdef set component=set([node])
        cdef set toexplore=set([node])
        cdef int n
        cdef int v 
        
        assert nodePredicate is None or nodePredicate(node)
        
        
        while toexplore:
            n = toexplore.pop()
            for v in self.neighbourIterator(n,nodePredicate, edgePredicate):
                if v not in component:
                    toexplore.add(v)
                    component.add(v)

            for v in self.parentIterator(n,nodePredicate, edgePredicate):
                if v not in component:
                    toexplore.add(v)
                    component.add(v)
                    
        return component
                
        
        
    
    def nodeIterator(self,predicate=None):
        return NodeIterator(self,predicate)
                
    def edgeIterator(self,nodePredicate=None, edgePredicate=None):
        cdef tuple edge
        cdef bytes key1
        cdef bytes key2
        cdef int   node1
        cdef int   node2
        
        for edge in self._edges_attrs:
            key1 = edge[0]
            key2 = edge[1]
            
            node1 = atol(key1)
            node2 = atol(key2)
            
            if nodePredicate is None or (nodePredicate(node1) and nodePredicate(node2)):
                edge = (node1,node2,0)
                if edgePredicate is None or edgePredicate(edge):
                    yield edge
                                
    def parentIterator(self,int node,nodePredicate=None, edgePredicate=None):
        cdef char[50] buffer
        cdef bytes key
        cdef set neighbours
        cdef int n 
        
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        neighbours = self._nodes[key][1]
        
        for key in neighbours:
            n = atol(key)
            if nodePredicate is None or nodePredicate(n):
                if edgePredicate is None or edgePredicate((n,node)):
                    yield n
                
    def neighbourIterator(self,int node,nodePredicate=None, edgePredicate=None):
        cdef char[50] buffer
        cdef bytes key
        cdef set neighbours
        cdef int n 
        
        
        snprintf(buffer,50,b"%d",node)
        key = buffer
        
        neighbours = self._nodes[key][0]
        
        for key in neighbours:
            n = atol(key)
            if nodePredicate is None or nodePredicate(n):
                if edgePredicate is None or edgePredicate((node,n)):
                    yield n
                    

    def connectedComponentIterator(self,nodePredicate=None, edgePredicate=None):
        cdef NodeIterator ni=self.nodeIterator(nodePredicate)
        cdef set cc
        cdef int n
        
        for n in ni:
            cc = self.connectedComponent(n,nodePredicate,edgePredicate)
            ni|=cc
            yield cc
            
        
        
    def __len__(self):
        return self.nodeCount()
    
    def __iter__(self):
        return self.nodeIterator()
            
    
    def __getitem__(self,key):
        cdef int   node1
        cdef int   node2
                
        if isinstance(key,tuple):
            node1 = key[0]
            node2 = key[1]
            
            return self.getEdgeAttr(node1,node2)
        
        elif isinstance(key,int):
            node1 = key

            try : 
                return self.getNodeAttr(node1)
            except IndexError as e:
                raise IndexError("%s --> index requested %d : %d" % (e.args[0],node1,key))
            
        raise TypeError("key must be an int or a tuple")

    def __str__(self):
        return self.dot()
    
    def __delitem__(self, int node):
        self.deleteNode(node)
        
    def minpath(self,source,dest = None, distance=None, nodePredicate=None, edgePredicate=None, allowCycle=False):
        cdef dict dist
        cdef dict previous
        cdef int32_t v 
        cdef FibonacciMinIntHeap Q = FibonacciMinIntHeap(chunksize=self.nodeCount()+1)
        cdef size_t d 
        cdef int32_t u
        cdef set idest
        
        def defaultdist(int32_t a, int32_t b):
            return 1
        
        if distance is None:
            distance=defaultdist
            
        dist={}
        previous={}
        
        for v in self.nodeIterator(nodePredicate):
            Q.push(v,INT32_MAX)
           
        idest = None 
        if dest is not None:
            idest=set(dest)
            
        if isinstance(source, int):
            source=set([source])
        else:
            source=set(source)
            
        for s in source:
            Q[s]=0
        
        while Q and (idest is None or dest):
            u,d = Q.pop()
            
            if d == INT32_MAX or (idest is not None and not idest):
                break
            
            dist[u]=d
            
            for v in self.neighbourIterator(u,nodePredicate, edgePredicate):
                if v in Q:
                    alt = d + distance(u,v)
                    if alt < Q.getPriority(v):
                        Q[v]=alt
                        previous[v]=u
                elif allowCycle and v in source:
                    alt = d + distance(u,v)
                    if alt < dist[v] or dist[v]==0:
                        dist[v]=alt
                        previous[v]=u
            
            if idest is not None and u in idest:
                idest.remove(u)

        idest = None 
        if dest is not None:
            idest=set(dist) - set(dest)
            for i in idest:
                del dist[i]
            
                        
        return dist,previous
                    
                    
    def __bytes__(self):
        return bytes(self.__str__.decode('latin1'))
        

def pathIterator(dist,previous):
    
    for p in dist:
        path=[p]
        while (p in previous):
            p= previous[p]
            path.append(p)
        path.reverse()
        yield path
        
                
        

        