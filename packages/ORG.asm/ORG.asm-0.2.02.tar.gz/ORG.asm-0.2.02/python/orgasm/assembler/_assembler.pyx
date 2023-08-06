# cython: language_level=3

cimport cython

from orgasm.indexer._orgasm cimport *
from ._asmbgraph cimport *
from ._assembler cimport *
from orgasm.graph._graphmultiedge cimport *
from functools import reduce

from orgasm.apps.progress cimport ProgressBar 
from orgasm.apps.config cimport getConfiguration 
from orgasm.utils.dna cimport reverseComplement
import math

import sys

from cpython.sequence cimport PySequence_GetSlice
from cpython.bytes cimport PyBytes_GET_SIZE


def cmp(a, b):
    return (a > b) - (a < b)

cdef int iabs(int x):
    return x if x > 0 else -x

@cython.nonecheck(True)
cdef tuple findDeepestRead(Index index, bytes seed):
    cdef list frg
    cdef list fcount
    cdef int mfc
    cdef int readsize=index.getReadSize()
    cdef int x
    cdef bytes b
    
    frg   = [PySequence_GetSlice(seed,x,(x+readsize)) for x in range(PyBytes_GET_SIZE(seed)-readsize)]
    fcount= [index.count(b) for b in frg]
    mfc = max(fcount)
    return frg[fcount.index(mfc)],mfc

cpdef cmpPoints(p1,p2):
    '''
    Compare two extensions point.
    INTERNAL functio uses for ordering extension point:
    the smallest point is point closest to the initial extension point
    with the highest coverage.
    
    :param p1:
    :type p1:
    :param p2:
    :type p2:
    '''
    
    rep = cmp(p2[0],p1[0])
    if not rep:
        rep= cmp(p1[4],p2[4])
    return -rep

def cmpRead(r1,r2):
    return cmp(r1[1],r2[1])


cdef int32_t deleteBranch(AsmbGraph graph,list path, int32_t maxlength, int32_t deleted=0):
    
    cdef int32_t   node
    cdef list      parents
    cdef list      sons
    cdef int32_t   i
    
    if len(path) > maxlength:
        return deleted
        

    node = path[-1]
    parents = [y for y in graph.parentIterator(node)]
    if parents :
        for p in parents:                
            sons    = [y for y in graph.neighbourIterator(p)]

            path+=[p]

            if len(sons) < 2:
                deleted = deleteBranch(graph,path,maxlength,deleted)
            else:
                for i in range(len(path)-1,0,-1):
                    try:
                        graph.deleteEdge(path[i],path[i-1])
                        deleted+=1
                    except KeyError:
                        pass
    else:
        for i in range(len(path)-1,0,-1):
            try:
                graph.deleteEdge(path[i],path[i-1])
                deleted+=1
            except KeyError:
                pass
        
    return deleted


cdef set sons(AsmbGraph graph,int node):                          # @DuplicatedSignature
    '''
    Build a set composed of the following reads  
    '''
    return set(graph.neighbourIterator(node))
    
cdef set parents(AsmbGraph graph,int node):                       # @DuplicatedSignature
    '''
    Build a set composed of the previous reads  
    '''
    return set(graph.parentIterator(node))

cdef bint is_junction(AsmbGraph graph,int node):                   # @DuplicatedSignature
    '''
    Predicate testing if a node is a fork or the beginning of the assembly
    '''
    return  (    len(sons(graph,node)) > 1 
              or len(parents(graph,node)) != 1 
            )

cdef bint is_begining(AsmbGraph graph,int node):                   # @DuplicatedSignature
    '''
    Predicate testing if a node is a fork or the beginning of the assembly
    '''
    return  len(parents(graph,node)) == 0 
            

cdef tuple normalizePath(list path, bint *direction):
    cdef int  c = path[0]
    cdef int  r = -path[-1]
    cdef bint d = c < r
    cdef tuple cpath
    
    
    # TODO: verify the property : if more than two nodes are reverse complement then the stem is palindromic 
    if c==r:
        c = path[1]
        r = -path[-2]
        d = c < r
    
    if d:
        cpath=tuple(path)
    else:
        cpath=tuple(-i for i in reversed(path))

    direction[0]=d
    return cpath

cdef bint isPalindrome(list path):
    cdef int lp = len(path)
    cdef int i
    # paths with a odd length cannot be palindromic 
    if (lp & 1) == 1:
        return False
    
    for i in range(lp//2):
        if path[i]!=-path[-i-1]:
            return False
        
    return True

cdef int weight(Assembler assembler,
                list      path,
                bint      palindrome):
    cdef float weight=0
    cdef int x 
    cdef AsmbGraph graph = assembler._graph
    cdef dict nattr
    cdef int nodemax = len(assembler._index) +1 
    
    for x in path:
        if iabs(x) < nodemax:
            nattr = graph.getNodeAttr(x)
            weight+=nattr.get('coverage',0.0)
           
    weight/= len(path)
    
    if palindrome:
        weight/=2
    
    return <int> (weight * assembler._index.getReadSize())
    
cdef str label(dict stem):
        cdef str label
        cdef int length = stem['length']
        
        if length > 10:
            label="%d : %s->(%d)->%s  [%d]" % (stem['stemid'],
                                               stem['sequence'][0:5].decode('ascii'),
                                               length,
                                               stem['sequence'][-5:].decode('ascii'),
                                               int(stem['weight'])
                                         )
        else:
            label="%d : %s->(%d)  [%d]" % (stem['stemid'],
                                           stem['sequence'].decode('ascii'),
                                           length,
                                           int(stem['weight'])
                                          )
            
        return label


cpdef dict buildstem(Assembler assembler,
               int first,
               int last,
               bytes sequence,
               list path,
               bint circle):
    
    cdef bint palindrome = isPalindrome(path)    
    cdef int w = weight(assembler,path,palindrome)
    cdef int  length = len(sequence)
    cdef dict s = { 'first'      : int(first),
                    'last'       : int(last),
                    'sequence'   : sequence,
                    'length'     : int(length),
                    'path'       : path,
                    'palindrome' : bool(palindrome),
                    'weight'     : int(w),
                    'circle'     : bool(circle),
                    'stemid'     : 0,
                    'label'      : None,
                    'head'       : assembler._index.getRead(first,
                                                            0,
                                                            assembler._index.getReadSize())
                  }
                
    if circle:
        getConfiguration()['orgasm']['logger'].info(" Circle : %6d bp coverage : %6dx" % 
              (length,int(w))) 
        
    return s   

cdef class CompactAssembling(DiGraphMultiEdge):


    def __init__(self,
                 Assembler assembler,
                 bint verbose=True
                ):
        
        cdef int n=0
        cdef int x
        cdef int i                                   # @DuplicatedSignature
        cdef lcontig=0
        cdef int first 
        cdef int last                                # @DuplicatedSignature
        cdef int lseq                                # @DuplicatedSignature
        cdef int lgraph
        cdef int lpath
        cdef bytes sequence                          # @DuplicatedSignature
        cdef dict attr                               # @DuplicatedSignature
        cdef double weight
        cdef double minweight
        cdef AsmbGraph graph
        cdef dict stem
        cdef dict config=getConfiguration()
        
        logger = config['orgasm']['logger']
         
        DiGraphMultiEdge.__init__(self,'compact')
        
        self._paths={}
        self._stemid={}
        self._stemidOk=False
        self._assembler=assembler
        
        graph = assembler._graph
        lgraph=len(graph)


        if verbose:
            logger.info("Compacting graph :")
        else:
            progress = ProgressBar(lgraph,
                                   head="Compacting graph",
                                   seconde=0.1)

        minweight=1000000.
        
        for stem in StemIterator(assembler):
            self.addStem(stem) 
            lcontig+=stem['length']
            weight = stem['weight']
            stem['graphics']={'width':(weight//assembler._index.getReadSize())+1,
                              'arrow':'last'
                             }

            if weight < minweight:
                minweight=weight

            if verbose:
                logger.info(" Stem  : %6d bp (total : %6d) coverage : %6.2f" % (stem['length'],
                                                                                lcontig,
                                                                                weight))
            else:
                progress(lcontig)
           
        self.setStemid()            
             
        logger.info("Minimum stem coverage = %d" % int(minweight))
        
        

    cpdef dict addStem(self, dict stem):
        cdef char[50] buffer1
        cdef char[50] buffer2
        cdef bytes key1 
        cdef bytes key2 
        cdef tuple edge
        cdef list eattr
        cdef int eid
        cdef int first = stem['first']
        cdef int last  = stem['last']
        cdef bint d

        cpath = normalizePath(stem['path'],&d)
        self._paths[cpath] = self._paths.get(cpath,0) + 1
        self._stemidOk=False
        
        snprintf(buffer1,50,b"%d",first)
        key1 = buffer1
        
        snprintf(buffer2,50,b"%d",last)
        key2 = buffer2
        
        edge = (key1,key2)
        
        if edge not in self._edges_attrs:
            self.addNode(first)
            self.addNode(last)
        
            self._nodes[key1][0].add(key2)
            self._nodes[key2][1].add(key1)

            self._edges_attrs[edge]=[]
            
        eattr = self._edges_attrs[edge]
        
        eattr.append(stem)
    
        self._edgecount+=1
                
        return stem

    cpdef deleteEdge(self, int node1, int node2, int edge=-1):
        cdef dict stem
        cdef bint d
        stem = self.getEdgeAttr(node1,node2,edge)
        cpath = normalizePath(stem['path'],&d)
        self._paths[cpath]-=1
        if self._paths[cpath]==0:
            del self._paths[cpath]
            self._stemidOk=False
        
        DiGraphMultiEdge.deleteEdge(self,node1,node2,edge)
        
    

    cdef int getStemid(self, dict stem) except 0:
        cdef list path = stem['path']
        cdef bint d
        cdef tuple cpath
        cdef int stemid
        cdef list sstems
                        
        if not self._stemidOk:
            sstems=list(self._paths)
            sstems.sort()
            for i in range(len(sstems)):
                self._stemid[sstems[i]]=i+1
            self._stemidOk=True
                
        cpath = normalizePath(path,&d)                
        stemid = self._stemid[cpath]

        if not d:
            stemid=-stemid
                
        return stemid


    def stemIterator(self):
        cdef list stemps
        cdef dict stem
        for stems in self._edges_attrs.values():
            for stem in stems:
                yield stem
        
    cdef void setStemid(self):
        cdef dict stem
    
        for stem in self.stemIterator():
            stem['stemid'] = self.getStemid(stem)
            stem['label']  = label(stem)


    
cdef class StemIterator:

    def __init__(self,Assembler assembler, 
                      bint alllink=False):
        self._assembler=assembler
        self._graph=assembler._graph
        self.edgeName={}
                            
    def __iter__(self):
        cdef NodeIterator ni
        cdef int first
        cdef int n
        cdef set branches
        cdef set brothers
        cdef set fathers
        cdef list lsequence
        cdef int last
        cdef int lseq
        cdef bytes sequence
        cdef list path
        cdef dict stem 
        cdef int lcontig
        cdef AsmbGraph graph =  self._graph
        cdef set junctions = set(int(y) for y in graph.nodeIterator(lambda x: is_junction(graph,x)))
                

        for first in junctions:
            branches=sons(graph,first)
            for n in branches:
                path = [first,n]                               
                brothers=sons(graph,n)
                lsequence=[graph.getEdgeAttr(first,n)['ext']]
                while len(brothers)==1 and n not in junctions:
                    son=brothers.pop()
                    lsequence.append(graph.getEdgeAttr(n,son)['ext'])
                    path.append(son)
                    n=son
                    brothers=sons(graph,n)
    
                last = n
                sequence=b''.join(lsequence)

                stem = buildstem(self._assembler,
                            first,last,
                            sequence,path,
                            False)
                
                lcontig+=stem['length']
                                
                yield stem
                                
                if stem['palindrome']:
                    yield stem
                    
        if lcontig + 2 * len(self.edgeName) < len(graph):
            ccs = graph.connectedComponentIterator()
            
            for cc in ccs:
                circle = not any(is_junction(graph,x) for x in cc)

                if circle:
                    minabs = min(abs(i) for i in cc)
                    if minabs in cc:
                        first = minabs
                    else:
                        first = sons(graph,-minabs).pop()
                    nn = first
                    path=[first]
                    lsequence=[]
                    son=sons(graph,nn).pop()
                    while first != son:
                        path.append(son)
                        lsequence.append(graph.getEdgeAttr(nn,son)['ext'])
                        nn=son
                        son=sons(graph,nn).pop()
    
                    last = first
                    sequence=b''.join(lsequence)
                    
                    stem = buildstem(self._assembler,
                                first,last,
                                sequence,
                                path,
                                True)
                
                    yield stem
                                                        
            


cdef class Assembler:
    '''
    totolitoto
    '''

    def __init__(self,Index index, int overlap=90):
        '''
        Create a new assembler object.
        
        :param index: the file name of an read index previously formated using orgasmi binary
        :type index: bytes
        :param seed: a DNA sequenced used as started for the assembly
        :type seed: bytes
        :param overlap: the minimum overlap between two reads
        :type overlap: int
        '''
        cdef bytes starter
        cdef int depth 
        cdef tuple reads
        cdef dict attr
                
        self._graph = AsmbGraph("assembling",index)
        
        self._index = index
        self._overlap=overlap
        self._seeds = []
        self._annotations = {}
                        
        
        
    cpdef tuple readType(self,ids):
        '''
        Internal function : Given a set of read ids, return the one that have to be used
        as standard id. 
         
        The set of ids given to this function corresponds to a set of all strictly identical reads.
          
        :param ids: an iterable elements contining read ids.
        :type ids: iterable
         
        :returns: a tuble of three elements
         
                    - the standard id to use
                    - the length of ids
                    - a set containing all unique ids given as parameter
                     
        :rtype: tuple
        '''
         
        cdef int t 
        cdef int y 
         
        if not ids:
            return None
         
        t = len(self._index)+1
         
        for y in ids:
            if abs(y) < abs(t):
                t = y
                 
        return (t,len(ids),set(ids))
    
    def isEnd(self, int node):
        cdef list s
        cdef list f
        s = [x for x in self.graph.neighbourIterator(node)]
        f = [x for x in self.graph.parentIterator(node)]
        if len(s)==0 and len(f)==1:
            return f[0]
        return 0

    def forkIterator(self):
        
        def has_several_sons(int node):
            return  len(set(self._graph.neighbourIterator(node))) > 1
        
        return self._graph.nodeIterator(has_several_sons)
    
        

           
    def endNodeSet(self, set excluded=None, bint alllink=False):
        if alllink:
            def isfinalnode(int node):
                return len(set(self._graph.neighbourIterator(node)))==0
        else:
            def isfinalnode(int node):                  # @DuplicatedSignature
                return len(set(self._graph.neighbourIterator(node)))==0
        if excluded is None:
            excluded=set()
        return set(x for x in self._graph.nodeIterator(isfinalnode) if x not in excluded)

    def startNodeSet(self, set excluded=None, bint alllink=False):
        if alllink:
            def isstartnode(int node):
                return len(set(self._graph.parentIterator(node)))==0
        else:
            def isstartnode(int node):                  # @DuplicatedSignature
                return len(set(self._graph.parentIterator(node)))==0
            
        if excluded is None:
            excluded=set()
        return set(x for x in self._graph.nodeIterator(isstartnode) if x not in excluded)

    def cleanDeadBranches(self,int32_t maxlength=10, bint alllink=False):

        cdef AsmbGraph graph
        cdef int32_t   d
        cdef int32_t   cd
        cdef int32_t   i                                # @DuplicatedSignature
        cdef set       ep
        cdef set       sp
                   
        graph=self.graph

        cd=0    
        d=1
            
        if sys.stderr.isatty():
            print('',file=sys.stderr)
        
        while d > 0:
            d=0
            
            for i in self.endNodeSet(alllink=alllink):
                if sys.stderr.isatty():
                    print("Remaining edges : %d node : %d" % (graph.edgeCount(),len(graph)),
                          end='\r',
                          file=sys.stderr)
                d+=deleteBranch(graph,[i],maxlength)
            cd+=d
            
        
        ep = self.endNodeSet(alllink=alllink)
        sp = self.startNodeSet(alllink=alllink)
        
        for i in ep & sp:
            try:
                graph.deleteNode(i)
            except KeyError:
                pass
            
        if sys.stderr.isatty():
            print ("Remaining edges : %d node : %d" % (graph.edgeCount(),len(graph)),
                   end='\r',
                   file=sys.stderr)

        return cd            
                
    def __len__(self):
        return self._graph.nodeCount()
            
    def compactAssembling(self, bint verbose=True):
        return CompactAssembling(self,verbose)
    
    
    property graph:

        "A doc string can go here."

        def __get__(self):
            return self._graph


    property seeds:

        "A doc string can go here."

        def __get__(self):                              # @DuplicatedSignature
            return self._seeds


    property index:

        "A doc string can go here."

        def __get__(self):                              # @DuplicatedSignature
            return self._index



                       
