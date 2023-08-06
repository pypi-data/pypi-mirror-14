# cython: language_level=3

from ._ahocorasick cimport *
from orgasm.apps.progress cimport ProgressBar 

from orgasm.utils.dna import reverseComplement
from ._bitvector cimport BitVector

import time
import math

#
# This dict is a mix off all mitochondrial, chroroplast and the universal genetic code
# It serves for back translating purpose
#
 
cdef dict UniversalGeneticCode     = {b"A" : (b"GCT", b"GCC", b"GCA", b"GCG"),
                                      b"C" : (b"TGT", b"TGC"),
                                      b"D" : (b"GAT", b"GAC"),
                                      b"E" : (b"GAA", b"GAG"),
                                      b"F" : (b"TTT", b"TTC"),
                                      b"G" : (b"GGT", b"GGC", b"GGA", b"GGG"),
                                      b"H" : (b"CAT", b"CAC"),
                                      b"I" : (b"ATT", b"ATC", b"ATA"),
                                      b"K" : (b"AAA", b"AAG"),
                                      b"L" : (b"TTA", b"TTG", b"TAG", b"CTT", b"CTC", b"CTA", b"CTG"),
                                      b"M" : (b"ATG", b"ATA"),
                                      b"N" : (b"AAT", b"AAC", b"AAA"),
                                      b"P" : (b"CCT", b"CCC", b"CCA", b"CCG"),
                                      b"Q" : (b"CAA", b"CAG"),
                                      b"R" : (b"CGT", b"CGC", b"CGA", b"CGG", b"AGA", b"AGG"),
                                      b"S" : (b"TCT", b"TCC", b"TCA", b"TCG", b"AGT", b"AGC", b"AGA", b"AGG"),
                                      b"T" : (b"ACT", b"ACC", b"ACA", b"ACG", b"CTT", b"CTC", b"CTA", b"CTG"),
                                      b"V" : (b"GTT", b"GTC", b"GTA", b"GTG"),
                                      b"W" : (b"TGA", b"TGG"),
                                      b"Y" : (b"TAT", b"TAC", b"TAA"),
                                     }

cdef dict CompUniversalGeneticCode = {b"A" : (b"AGC", b"GGC", b"TGC", b"CGC"),
                                      b"C" : (b"ACA", b"GCA"),
                                      b"D" : (b"ATC", b"GTC"),
                                      b"E" : (b"TTC", b"CTC"),
                                      b"F" : (b"AAA", b"GAA"),
                                      b"G" : (b"ACC", b"GCC", b"TCC", b"CCC"),
                                      b"H" : (b"ATG", b"GTG"),
                                      b"I" : (b"AAT", b"GAT", b"TAT"),
                                      b"K" : (b"TTT", b"CTT"),
                                      b"L" : (b"TAA", b"CAA", b"CTA", b"AAG", b"GAG", b"TAG", b"CAG"),
                                      b"M" : (b"CAT", b"TAT"),
                                      b"N" : (b"ATT", b"GTT", b"TTT"),
                                      b"P" : (b"AGG", b"GGG", b"TGG", b"CGG"),
                                      b"Q" : (b"TTG", b"CTG"),
                                      b"R" : (b"ACG", b"GCG", b"TCG", b"CCG", b"TCT", b"CCT"),
                                      b"S" : (b"AGA", b"GGA", b"TGA", b"CGA", b"ACT", b"GCT", b"TCT", b"CCT"),
                                      b"T" : (b"AGT", b"GGT", b"TGT", b"CGT", b"AAG", b"GAG", b"TAG", b"CAG"),
                                      b"V" : (b"AAC", b"GAC", b"TAC", b"CAC"),
                                      b"W" : (b"TCA", b"CCA"),
                                      b"Y" : (b"ATA", b"GTA", b"TTA"),
                                     }


cdef dict listCodons2Dict(tuple codons):
    cdef dict d={}
    cdef dict s
    cdef dict new
    cdef char* cc
    cdef dict      value
    cdef int  l
    cdef char letter[2]
    cdef bytes c

    letter[1]=0
    
    for c in codons:
        s = d
        cc= c
        for l in range(3):
            letter[0]=cc[l]
            value = s.get(letter,None)
            if value is None:
                value = {}
                s[letter]=value
            s=value
                
    return d

cpdef dict bindCodons(dict codon1, dict codon2):
    cdef PyObject* pkey
    cdef bytes     key
    cdef PyObject* pvalue  # @DuplicatedSignature
    cdef dict      l2
    cdef dict      l3
    cdef Py_ssize_t ppos1=0
    cdef Py_ssize_t ppos2=0
    cdef Py_ssize_t ppos3=0
    
    while PyDict_Next(codon1, &ppos1, &pkey, &pvalue):
        l2=<object>pvalue
        ppos2=0
        while PyDict_Next(l2, &ppos2, &pkey, &pvalue):
            l3=<object>pvalue
            ppos3=0
            while PyDict_Next(l3, &ppos3, &pkey, &pvalue):
                Py_XDECREF(pvalue)
                key=<object>pkey
                PyDict_SetItem(l3,key,codon2)

    return codon1

cpdef dict codon(char aa, bint direct=True):
    cdef tuple value
    cdef char  letter[2]
    
    letter[0]=aa
    letter[1]=0
    
    
    if direct:
#        value = <object>PyDict_GetItemString(UniversalGeneticCode,letter)
        value = UniversalGeneticCode[letter]
    else:
#        value = <object>PyDict_GetItemString(CompUniversalGeneticCode,letter)        
        value = CompUniversalGeneticCode[letter]        
    
    return listCodons2Dict(value)

cpdef bint homopolymer(bytes s):
    """
    Returns True if the word s is an homopolymer, an homedimer 
    or an homotrimer
    
    @param s: the string to test
    @type s: bytes   
    
    @return True if s is an homopolymer, an homedimer 
            or an homotrimer, False otherwise
    @rtype: bool
    """
    s2 = s[2:] + s[0:2]
    s3 = s[3:] + s[0:3]
    return s==s2 or s==s3
                
def enumerateword(dict automata, bytes prefix=b""):
    cdef bytes k
    cdef bytes w 
    
    if not automata:
        yield prefix
    else:
        for k in automata:
            for w in enumerateword(automata[k],prefix+k):
                yield w
          
cpdef dict word2automata(wordlist):
    cdef dict automata={}
    cdef bytes w
    cdef dict  a 
    cdef bytes l 
    cdef dict  d
    
    for w in wordlist:
        a = automata
        for l in w:
            d = a.get(l,{})
            a[l]=d
            a=d
            
    return automata

cdef double* buildShanonTable(size_t readsize, size_t* offset):
    cdef size_t codonmax = readsize // 3 + (1 if (readsize % 3) else 0)
    cdef size_t i=codonmax+1
    cdef size_t j=0
    cdef size_t k=0
    cdef double* table
    cdef double* line
    cdef double log6=log(6)
    cdef double freq
    
    while i!=0:
        k|=(i & 1) & (i>1)
        i >>= 1
        j+=1
        
    j+=k
    
    offset[0]=j
    codonmax=1<<j
        
    table = <double*> malloc((readsize+1)*(codonmax)*sizeof(double))
    
    for i in range(readsize+1):
        line = table + (i << offset[0])
        for j in range(codonmax):
            if j <=i and j > 0:
                freq = <double> j / <double> i
                freq = -freq * log(freq)/log6
            else:
                freq=0
            line[j]=freq 
            
    return table
            
    
 
cdef bint samereads(unsigned char* p1, unsigned char* p2, size_t length):
    cdef uint64_t *w1 = <uint64_t*>p1
    cdef uint64_t *w2 = <uint64_t*>p2
    cdef size_t   i
    
    for i in range(length):
        if w1[i]!=w2[i]:
            return False
        
    return True   

cdef class AhoCorasick:
    
    def __init__(self,initsize=100000):
        self._finalized = False
        self._step = initsize
        self._depth= 0
        self._maxseqid=0
        self._maxpos=0
        
        # Allocate state arena
        
        self._states = <dnastate*> malloc(sizeof(dnastate)
                                          * initsize)
        
        if self._states==NULL:
            raise RuntimeError("No more memory for automata states")
        
        self._statesize = initsize
        
        # initialize initial state
        
        self._states.match = <protmatch*>-1
        self._states.a     = NULL
        self._states.c     = NULL
        self._states.t     = NULL
        self._states.g     = NULL
        
        self._seqid       = {}
        self._rseqid       = {}
        
        self._statecount = 1
        
        # allocate match arena
        
        self._matches = <protmatch*> malloc(sizeof(protmatch)
                                            * initsize)
        
        if self._matches==NULL:
            raise RuntimeError("No more memory for automata matches")
        
        self._matchsize = initsize
        self._matchcount= 0
        
        
        
    def __dealloc__(self):
        if (self._states != NULL):
            free(<void*>self._states)
        if (self._matches != NULL):
            free(<void*>self._matches)
            
            
    def __len__(self):
        return self._statecount
    
    def addWord(self,bytes word,int protid, int position):
        cdef char* cword = word 
        
        assert not self._finalized, "You cannot add words to a finilized automata"

        self.addCWord(cword,PyBytes_Size(word),protid,position)


    cdef dnastate *getNextState(self,dnastate *base, int letter):
        cdef dnastate** table=&(base.a)
        cdef dnastate*  state = table[letter]
        cdef dnastate*  arena
        cdef size_t     baseid    
    
        if state == NULL:
            if self._finalized:
                return NULL
            else:
                                
                if self._statecount == self._statesize:
                    #
                    # the state arena if full we need to enlarge it
                    #
                    
                    # we save baseid to convert it to the new arena adressing system 
                    baseid = base - self._states
                    
                    # new size of the arena and correponding allocation
                    self._statesize+=self._step
#                    print "realloc buffer to size %d" % self._statesize
                    arena = <dnastate*> realloc(self._states,
                                                sizeof(dnastate)
                                                * self._statesize)
                                         
                    if arena == NULL:
                        # We were not able to enlarge arena
                        return NULL
                    else:
                        self._states = arena
                       
                    #compute the new base and table address
                    base = arena + baseid
                    table=&(base.a)
                
                state = self._states + self._statecount
                table[letter] = <dnastate*>self._statecount
                self._statecount+=1
                
                state.match = <protmatch*>-1
                state.a     = NULL
                state.c     = NULL
                state.t     = NULL
                state.g     = NULL
                
                return state
                
        else:
            if self._finalized:
                return state 
            else:
                return self._states + <size_t> state
            
    cdef protmatch* setAsTerminal(self, dnastate* base, int protid, int position):
        """
        setAsTerminal function is an internal function that is called from the
        addWord method. It must be only used on none finalized automata, but 
        no checking for this property is done a precondition
        """
        cdef protmatch* curmatch = NULL
        cdef protmatch* nextmatch= NULL
        cdef size_t     curmatchid
        cdef protmatch* arena
        
        if position > self._maxpos:
            self._maxpos = position 
        
        if base.match!=<protmatch*>-1:
            nextmatch = self._matches + <size_t>(base.match)        
        
        while(nextmatch):
            curmatch = nextmatch
            if (    curmatch.protid == protid 
                and curmatch.position == position):
                return curmatch
            else:
                if curmatch.next:
                    nextmatch = self._matches + <size_t>curmatch.next
                else:
                    nextmatch = NULL
                    
        # There no match for position@protid register to this state
        # so we have to create a new one
            
        if self._matchcount == self._matchsize:
            # I save the curmatchid to restore curmatch later
            if curmatch :
                curmatchid = curmatch - self._matches
                        
            # the match arena if full we need to enlarge it
            
            self._matchsize+=self._step
#            print "reallocate matches to %d" % self._matchsize
            arena = <protmatch*> realloc(self._matches,
                                         sizeof(protmatch)
                                         * self._matchsize)
                                 
            if arena == NULL:
                # We were not able to enlarge arena
                return NULL
            else:
                self._matches = arena
                
            # I restore curmatch 
            if curmatch :
                curmatch = self._matches + curmatchid

                
        # compute the address 
        nextmatch = self._matches + self._matchcount
        
        if curmatch : 
            curmatch.next = <protmatch*>self._matchcount
        else:
            base.match = <protmatch*>self._matchcount
            
        self._matchcount+=1
        
        nextmatch.protid = protid
        nextmatch.position = position 
        nextmatch.next = NULL 
        
        if protid > self._maxseqid:
            self._maxseqid=protid
        
        return nextmatch 
    
    cdef dnastate* simpleMatch(self,char* cword, size_t lword):
        """
        Checks if cword a dna word of length lword is present in 
        the automata. The function returns the state at the end of
        the word in the automata or null if the word is not found

        This function is used for computing the error link during the
        finalization step
        
        warning : This is a private function that should not be used directly        
        """
        cdef char   letter
        cdef dnastate** table
        cdef dnastate*  curstate
        cdef dnastate*  nextstate
                
        # We cannot match a word of length null
        # neither longer than the longest pattern
        # in the automata
        
        if lword>self._depth:
            return NULL 
        
        nextstate = self._states 
        
        while (nextstate!=NULL and lword):
            curstate = nextstate

            letter = cword[0]
            table    = &(curstate.a)
            nextstate = table[letter]
            
            cword+=1
            lword-=1
            
        if lword==0 and nextstate!=NULL:
            return nextstate
        else:
            return NULL
        
        
    cdef dnastate* longestSuffix(self,char* cword, size_t lword):
        """
        identify the longest suffix of cword that is recognized by
        the Aho-Corasick automata.
        
        This function is used for computing the error link during the
        finalization step
        
        warning : This is a private function that should not be used directly        
        """
        cdef dnastate* suffix=NULL

        
        while lword >= 1 and suffix==NULL:
            cword+=1
            lword-=1

            suffix = self.simpleMatch(cword,lword)
            
        return suffix
            
        
    cdef setErrorLink(self):
        """
        Add error link to the Aho-Corasick automata during its finalization
        step.
        
        warning : This is a private function that should not be used directly
        """
        cdef char* buffer
        cdef size_t*     stack
        cdef dnastate*  curstate
        cdef dnastate*  nextstate
        cdef dnastate** table
        cdef dnastate* links
        cdef dnastate** errors
        cdef size_t i
        cdef size_t j
        cdef int pos=0
        cdef size_t lsuffix
        cdef size_t lword
         

#        print "depth : %d -> %d" % (self._depth,sizeof(size_t)*(self._depth+1)*4)

        stack = <size_t*>malloc(sizeof(size_t)*(self._depth+1)*4)

        errors = <dnastate**>malloc(sizeof(dnastate*) * self._statecount)
        bzero(<void*>errors,sizeof(dnastate*) * self._statecount)
        
        buffer=<char*>malloc(sizeof(char)*(self._depth+1))

        #
        # We explore trie with a deep first algorithm
        #
        
        # I put on the stack the root of the automata
        stack[0] = 0
        pos = 0

        j=0 # used to scan the four branches of a node     
       

        while pos >= 0:
#            print "Run on state : [%d]  %d-%d" % (pos,stack[pos],j)

            # I consider the last state on the stack 
            curstate = self._states + stack[pos] 
            table=&(curstate.a)          
            
            # We skip the empty link
            while j < 4 and table[j]==NULL:
                j+=1
                
            # on the loop exit or j==4 and we have explored all the branches
            # or j<4 and we found a non empty branch
                
            if j < 4:
                
                # We found a link we push it on the stack
                
                buffer[pos]=j
                pos+=1
                stack[pos]= (table[j] - self._states)
#                print "push %d [%d]" % (pos,j)
                j=0
                            
                # ===> Then we loop on the main while
                
            else:
                
                # There is no more link on this state
                # --> we cannot go deeper
                                
                links = self.longestSuffix(buffer,pos)
                errors[stack[pos]]=links
                                           
                # we pop out the state
                pos-=1
                j = buffer[pos]+1
         
        errors[0]=NULL       

#        for i in range(1,self._statecount):
#            if errors[i]==NULL:
#                print "no link on %d" % i
                
        for i in range(self._statecount):
            curstate=self._states + i 
            for j in range(4):
                nextstate=curstate
                table=&(nextstate.a)
                if table[j]==NULL:
                    while nextstate!=NULL and table[j]==NULL:
                        nextstate = errors[nextstate - self._states]
                        table=&(nextstate.a)
                    if nextstate==NULL:
#                        print "jump to %d[%d] -> root" % (i,j)
                        nextstate = self._states
                    else:
                        nextstate = table[j]
#                        print "jump to %d[%d] -> %d" % (i,j,nextstate-self._states)
                    table =&(curstate.a) 
                    table[j]=nextstate
                
                
        free(errors)
        free(stack)
        free(buffer)

    cpdef finalize(self):
        cdef size_t i 
        cdef size_t j 
        cdef size_t dest
        cdef dnastate* state
        cdef dnastate** table
        cdef protmatch* match
        
        if self._finalized:
            return None
        
        self._finalized = True

        for i in range(self._statecount):
            state = self._states + i
            
            if state.match!=<protmatch*>-1:
                state.match = self._matches + <size_t>state.match
            else:
                state.match = NULL
                
            table=&(state.a)
            for j in range(4):
                if table[j]!=NULL:
                    table[j]=self._states + <size_t>table[j]
                    
        for i in range(self._matchcount):
            match = self._matches + i
            if match.next!=NULL:
                match.next=self._matches + <size_t>match.next
                                                            
        self.setErrorLink()          
        
      
    cdef int addCWord(self,char* cword, size_t lword, int protid, int position):
        cdef int   letter
        cdef int   i
        cdef dnastate* state = self._states
        cdef protmatch* match  # @DuplicatedSignature
                        
        for i in range(lword):
            letter = cword[i] 
            letter >>=1
            letter &=3
            state = self.getNextState(state,letter)
            
            if state==NULL:
                return 0
            
        match = self.setAsTerminal(state,protid,position)
            
        if match == NULL:
            return 0
         
        if lword > self._depth:
            self._depth=lword  
             
        return self._statecount
    
    
    cdef int addAutomata(self,dict automata,int protid, int position):
        cdef list       stack=[(automata,0,0)]
        cdef tuple      stackitem
        cdef PyObject*  pkey
        cdef char*      ckey  
        cdef int        letter
        cdef PyObject*  pvalue
        cdef dict       value
        cdef Py_ssize_t ppos=0
        cdef dnastate*  state
        cdef dnastate*  nstate
        cdef protmatch* match
        cdef size_t     stateid
        cdef size_t     lword=0
       
        while PyList_GET_SIZE(stack)>0 :
            stackitem = stack.pop()
            automata  = <object>PyTuple_GET_ITEM(stackitem,0)
            stateid   = PyInt_AsSsize_t(<object>PyTuple_GET_ITEM(stackitem,1))
            lword     = PyInt_AsSsize_t(<object>PyTuple_GET_ITEM(stackitem,2))
            state     = self._states + stateid
            ppos      = 0
            
            lword+=1
            
            while PyDict_Next(automata, &ppos, &pkey, &pvalue):
                
                if lword > self._depth:
                    self._depth=lword
                #
                # Get the nucleotide code
                #
                
                ckey = PyBytes_AS_STRING(pkey)
                letter = ckey[0]
                letter>>=1
                letter&=3
                
                #
                # create or gate the corresponding node in the automata
                #
                
                nstate = self.getNextState(state,letter)
                
                # potentially recompute state address if reallocation occured 
                state     = self._states + stateid
                
                if state==NULL:
                    return 0
                
                # 
                # if value is an empty dict then this is a terminal state
                # else we have to push it on the stack
                #
                
                value=<object>pvalue
                
#                print stateid,"->",(nstate - self._states),value
                
                if PyDict_Size(value):
                    stack.append((value,(nstate - self._states),lword))
#                    print "on continue"
                else:
#                    print "Etat final"
                    match = self.setAsTerminal(nstate,protid,position)       
#                    print "Etat final ok"
                    if match == NULL:
                        return 0
                   
        return self._statecount
                
        
    
    
    cpdef dict match(self,bytes sequence):
        cdef char*  csequence = sequence 
        cdef size_t lseq      = len(sequence)
        cdef size_t pos      
        cdef dnastate* state 
        cdef dnastate* nstate 
        cdef dnastate** table 
        cdef protmatch* pmatch
        cdef int letter
        cdef dict results = {}
        cdef PyObject*  plpos
        cdef list lpos
        cdef int protid
        
                
        if not self._finalized:
            self.finalize()
        
        state = self._states
        
        for pos in range(lseq):
            table = &(state.a)
            letter = csequence[pos]
            letter >>=1
            letter &=3
            nstate = table[letter]
            pmatch = nstate.match
            while (pmatch!=NULL):
                plpos = PyDict_GetItem(results,PyInt_FromLong(pmatch.protid))
                if plpos==NULL:
                    lpos = []
                    PyDict_SetItem(results,PyInt_FromLong(pmatch.protid),lpos)
                else:
                    lpos = <object>plpos
                lpos.append((pos,pmatch.position))
                pmatch = pmatch.next
            state = nstate
                    
        return results 
                
                
           
            
            
        
    
    cpdef DiGraphMultiEdge asGraph(self):
        cdef DiGraphMultiEdge g 
        cdef size_t i 
        cdef size_t j 
        cdef size_t dest
        cdef dnastate* ndest
        cdef dict node
        cdef dict edge
        cdef dnastate** table
        cdef protmatch* match
        cdef size_t matchcount = 0
        cdef size_t pnode
        
        g=DiGraphMultiEdge(b"AhoCorasick")
        
        for i in range(self._statecount):
            g.addNode(i)
            node=g.getNodeAttr(i)
            node[b'label'] = b"%d" % i
            node[b'graphics'] = {}
            if i==0:
                node[b'graphics'][b'fill']=b'#008000'
                node[b'graphics'][b'type']=b'rectangle'  
                
            match = self._states[i].match    
            if ((not self._finalized and match!=<protmatch*>-1) or
                (self._finalized and match!=NULL)):
                node[b'graphics'][b'fill']=b'#800000'
                node[b'graphics'][b'type']=b'triangle'
                
                if not self._finalized:
                    match = self._matches + <size_t>match
                
                pnode = i
                while(match!=NULL):
                    #print "%d" % <size_t>match
                    matchcount+=1
                    g.addNode(self._statecount + matchcount)
                    node = g.getNodeAttr(self._statecount + matchcount)
                    node[b'graphics'] = {"type" : 'circle',
                                         'fill' : "#000080"
                                        }
                    node[b'label'] = "%d,%d" % (match.protid,match.position)
                    g.addEdge(pnode,self._statecount + matchcount)  
                    edge = g.getEdgeAttr(pnode,self._statecount + matchcount)
                    edge['graphics']={b'arrow':b'last',
                                      b'fill':b'#000040'
                                     }            
                    pnode = self._statecount + matchcount
                    match = match.next
                    if match!=NULL and not self._finalized:
                        match = self._matches + <size_t>match
                
        for i in range(self._statecount):
            table=&(self._states[i].a)
            for j in range(4):
                if self._finalized:
                    ndest = table[j]
                    if ndest:
                        dest  = ndest - self._states
                    else:
                        dest = 0
                else:
                    dest  = <size_t>table[j]
                    ndest = <dnastate*>-1
                    if dest==0:
                        ndest=NULL
                    
                if ndest != NULL:
                    g.addEdge(i,dest)
                    edge = g.getEdgeAttr(i,dest)
                    edge[b"label"]=b'%s' % (b"actg"[j])
                    edge['graphics']={b'arrow':b'last',
                                      b'fill':b'#080000'
                                     }            
        
        return g
    

cdef class ProtAhoCorasick(AhoCorasick):

    cpdef int addSequence(self,bytes sequence, object seqid=1, size_t kup=4):
        cdef int   position
        cdef int   k
        cdef char* csequence
        cdef char  letter[2]
        cdef dict  c
        cdef int osize
        cdef size_t erreur
        cdef int   id
        
        if self._finalized:
            return 0
        
        
        if seqid in self._seqid:
            id = self._seqid[seqid]
        else:
            id = self._maxseqid + 1
            self._seqid[seqid]=id
            self._rseqid[id]=seqid
            
        # register the size of the automata before add the protein
                
        osize = self._statecount
        
        letter[1]=0
        csequence = sequence
                
        # Backtranslate according to the forward strand

        for position in range(len(sequence)-kup+1):
            
            # for each peptide of size kup build a small automata with all
            # codon variants
            
            c = codon(csequence[position+kup-1])
            
            for k in range(position+kup-2,position-1,-1):
                c = bindCodons(codon(csequence[k]),c)
                                                
            c = word2automata([w for w in enumerateword(c) if not homopolymer(w)])
            erreur = self.addAutomata(c, id, (position+kup) * 3 - 1)
            
            if erreur==0:
                return 0
                            
        # Backtranslate according to the reverse strand
                
        for position in range(len(sequence)-1,kup-2,-1):
            
            # for each peptide of size kup build a small automata with all
            # anticodon variants
            
            c = codon(csequence[position-kup+1],False)
            for k in range(position-kup+2,position+1):
                c = bindCodons(codon(csequence[k],False),c)
            
            c = word2automata([w for w in enumerateword(c) if not homopolymer(w)])

            erreur = self.addAutomata(c, -id, position * 3 + 2)
            if erreur==0:
                return 0

        return self._statecount - osize

    cpdef scanIndex(self,Index seqindex,int minmatch=15, int maxmatch=-1, int covmin=1, bint progress=True):
        """
        
        
            @param seqindex: A NGS read index
            @type seqindex: orgasm.indexer._orgasm.Index instance
            
            @param minmatch: minimum count of identified word to take into
                             account the match
            @type minimum: int
                             
            @param maxmatch: maximum count of identified word to take into
                             account the match. Repeated can leads to huge
                             wordcount without real similarity
                             By default (-1) this value is set to readsize/3
                             (I.e amino acid count).
            @type maximum: int
            
            @param covmin: minimum count observed for a read to be taken into 
                           account
            @type covmin: int
            
            @param progress: Boolean flg indicating if a progress bar must be
                             displayed
            @type progress: bool
        """
        cdef unsigned char* nucs
        cdef size_t i  # @DuplicatedSignature
        cdef size_t j  # @DuplicatedSignature
        cdef int k
        cdef list ks
        cdef size_t readcount  = seqindex._index.readCount
        cdef size_t recordsize = seqindex._index.recordSize
        cdef size_t readsize   = seqindex._index.readSize
        
        # the number of non-overlaping 4mer in a read
        cdef size_t readsize4  = (readsize >> 2) + (1 if (readsize & 3)  else 0)
        
        # the number of non-overlaping 32mer in a read
        cdef size_t readsize64 = (readsize >> 5) + (1 if (readsize & 31) else 0)
        
        # Pointer to the first read record
        cdef unsigned char*  records    = <unsigned char*>seqindex._index.records
        cdef unsigned char*  nuc4
        cdef unsigned char*  nuc4bis
        cdef BitVector   wordcount
        cdef size_t wordmax=0
        cdef double shamin
        cdef size_t wc[6]
        cdef size_t rp[6]
        cdef dict matchpos
        
        cdef size_t* count
        cdef int wct
        cdef int wcmax
        cdef int phase 
        cdef int protidmax=0
        cdef int framemax=0
        cdef int loc
        cdef int locmax
        
        cdef size_t nbreads
        cdef dnastate* state 
        cdef dnastate* nstate 
        cdef dnastate** table 
        cdef int letter
        cdef dict results = {}
        cdef int readid
        cdef PyObject*  plpos        
        cdef list lpos
        cdef int pid 
        cdef int p 
        cdef double  shanon
        cdef size_t  offset
        cdef double* shanonTable = buildShanonTable(readsize,&offset)
        cdef double* shanonLine
        cdef ProgressBar pb
        
        # mid is the number of read frame globally available for each 
        # protein stored in the automata
        cdef int mid = self._maxseqid * 6 + 3
        
        # Finalize the automata if needed
        if not self._finalized:
            self.finalize()
        
        # Computes the default maxmatch according to the read size
        if maxmatch < 0:
            maxmatch = readsize // 3
            
        i=0
        
        wordcount = BitVector(mid,self._maxpos)
        
        nuc4 = records + i * (recordsize)
        
        if (progress):
            pb=ProgressBar(readcount)
#            progressBar(1,readcount,True)

        while i < readcount:
                
            # We start a new read so we set counter to 0
            wordcount.clear()     
            matchpos={}   
            
            readid = i
#            print "@",i
            
            # setup automata to the initial state
            state = self._states
            table = &(state.a)
            for j in range(readsize4):
                nucs = <unsigned char*>&(expanded8bitsnuc[nuc4[j]])
                for k in range(4):
                    letter = nucs[k]
                    nstate = table[letter]
                    pmatch = nstate.match
                    while (pmatch!=NULL):
#                        print "coucou %d %d" %(pmatch.protid,pmatch.position)
                        pid = pmatch.protid * 3 + ((j*4+k) % 3)
                        if pid < 0 :
                            pid += mid
                        wordcount.set(pid,pmatch.position)
                        matchpos[pid]=min(matchpos.get(pid,65535),pmatch.position)
                        pmatch = pmatch.next
                    state = nstate
                    table = &(state.a)
                    
            shamin=1.0
            wordmax=0
            protidmax=0
            framemax=0
            
            count = wordcount.counter()
            
            for k in range(1,self._maxseqid+1):
                pid = k * 3
                
                wc[3]=count[pid]
                wc[4]=count[pid+1]
                wc[5]=count[pid+2]
                
                rp[3]=matchpos.get(pid,65535)
                rp[4]=matchpos.get(pid+1,65535)
                rp[5]=matchpos.get(pid+2,65535)
                
                #memcpy(<void*>(wc+3),<void*>(count+pid),3*sizeof(size_t))
                
                pid = mid - pid 
                 
                wc[0]=count[pid]
                wc[1]=count[pid+1]
                wc[2]=count[pid+2]

                rp[0]=matchpos.get(pid,65535)
                rp[1]=matchpos.get(pid+1,65535)
                rp[2]=matchpos.get(pid+2,65535)
                
                # memcpy(<void*>(wc),<void*>(count+pid),3*sizeof(size_t))
                
                wct = wc[0] + wc[1] + wc[2] + \
                      wc[3] + wc[4] + wc[5]
                                            
                if wct > minmatch:
                    shanonLine = shanonTable + (wct << offset)
                    shanon=shanonLine[wc[0]] + \
                           shanonLine[wc[1]] + \
                           shanonLine[wc[2]] + \
                           shanonLine[wc[3]] + \
                           shanonLine[wc[4]] + \
                           shanonLine[wc[5]]
                
                    wcmax=0
                    phase=0
                    for p in range(6):
                        if wc[p]>wcmax:
                            wcmax=wc[p]
                            phase=p-3
                            loc=rp[p]
                else:
                    shanon=1.0
                    wcmax=0
                    phase=0

                if ((shanon<0.1) and
                    (wcmax >=minmatch) and
                    (wcmax >wordmax)):
                    shamin = shanon
                    wordmax = wcmax
                    protidmax=k
                    framemax= phase
                    locmax=loc
                    

                
            nbreads=1
            nuc4bis=nuc4 + recordsize
            i+=1

            if (progress):
                pb(i)

            while (i< readcount and 
                   samereads(nuc4, nuc4bis, readsize64)):
                nbreads+=1
                nuc4bis+= recordsize
                i+=1
                
#            print "Best match : %d -> %d (%d)" % (protidmax,wordmax,nbreads) 

            nuc4 = nuc4bis
            
            if protidmax>0 and shamin < 0.1 and nbreads >= covmin:
                if framemax < 0:
                    readid = -readid - 1
                else:
                    readid+=1 
                    
                plpos = PyDict_GetItem(results,PyInt_FromLong(protidmax))
                if plpos==NULL:
                    lpos = []
                    PyDict_SetItem(results,PyInt_FromLong(protidmax),lpos)
                else:
                    lpos = <object>plpos
                lpos.append((readid,wordmax,nbreads,framemax,shamin,locmax))
        
        #<------------------------------ End of the while loop ------------------------>
                
        ks = list(results.keys())

        for k in ks:
            results[self._rseqid[k]]=results[k]
            del results[k]
        

        free(shanonTable)          
        return results
                
 
cdef class NucAhoCorasick(AhoCorasick):

    cpdef int addSequence(self,bytes sequence, object seqid=1, size_t kup=12):
        cdef int   position
        cdef int   k
        cdef char* csequence
        cdef char  letter[2]
        cdef dict  c
        cdef int osize
        cdef size_t erreur
        cdef int   id
        
        if self._finalized:
            return 0
        
        
        if self._seqid.has_key(seqid):
            id = self._seqid[seqid]
        else:
            id = self._maxseqid + 1
            self._seqid[seqid]=id
            self._rseqid[id]=seqid
            
        # register the size of the automata before add the protein
        
        osize = self._statecount
        
        # Backtranslate according to the forward strand

        for position in range(len(sequence)-kup+1):
            
            # for each peptide of size kup build a small automata with all
            # codon variants
            self.addWord(sequence[position:position+kup],id,position)
            self.addWord(reverseComplement(sequence[position:position+kup]),-id,position)

        return self._statecount - osize
    
    cpdef scanIndex(self,Index seqindex,int minmatch=5, int maxmatch=-1, int covmin=1, bint progress=True):
        """
        
        
            @param seqindex: A NGS read index
            @type seqindex: orgasm.indexer._orgasm.Index instance
            
            @param minmatch: minimum count of identified word to take into
                             account the match
            @type minimum: int
                             
            @param maxmatch: maximum count of identified word to take into
                             account the match. Repeated can leads to huge
                             wordcount without real similarity
                             By default (-1) this value is set to readsize/3
                             (I.e amino acid count).
            @type maximum: int
            
            @param covmin: minimum count observed for a read to be taken into 
                           account
            @type covmin: int
            
            @param progress: Boolean flg indicating if a progress bar must be
                             displayed
            @type progress: bool
        """
        cdef unsigned char* nucs
        cdef size_t i  # @DuplicatedSignature
        cdef size_t j  # @DuplicatedSignature
        cdef int k
        cdef list ks
        cdef size_t readcount  = seqindex._index.readCount
        cdef size_t recordsize = seqindex._index.recordSize
        cdef size_t readsize   = seqindex._index.readSize
        
        # the number of non-overlaping 4mer in a read
        cdef size_t readsize4  = (readsize >> 2) + (1 if (readsize & 3)  else 0)
        
        # the number of non-overlaping 32mer in a read
        cdef size_t readsize64 = (readsize >> 5) + (1 if (readsize & 31) else 0)
        
        # Pointer to the first read record
        cdef unsigned char*  records    = <unsigned char*>seqindex._index.records
        cdef unsigned char*  nuc4
        cdef unsigned char*  nuc4bis
        cdef BitVector   wordcount
        cdef size_t wordmax=0
        cdef double shamin
        cdef size_t wc[6]
        cdef size_t rp[6]
        cdef dict matchpos
        
        cdef size_t* count
        cdef int wct
        cdef int wcmax
        cdef int phase 
        cdef int protidmax=0
        cdef int framemax=0
        cdef int loc
        cdef int locmax
        
        cdef size_t nbreads
        cdef dnastate* state 
        cdef dnastate* nstate 
        cdef dnastate** table 
        cdef int letter
        cdef dict results = {}
        cdef int readid
        cdef PyObject*  plpos        
        cdef list lpos
        cdef int pid 
        cdef int p 
        cdef size_t  offset
        
        # mid is the number of read frame globally available for each 
        # protein stored in the automata
        cdef int mid = self._maxseqid * 2 + 1
        # Finalize the automata if needed
        if not self._finalized:
            self.finalize()
        
        # Computes the default maxmatch according to the read size
        if maxmatch < 0:
            maxmatch = readsize 
            
        i=0
        
        wordcount = BitVector(mid,self._maxpos)
        
        nuc4 = records + i * (recordsize)
        
        if (progress):
            pb=ProgressBar(readcount)

        while i < readcount:
                
            # We start a new read so we set counter to 0
            wordcount.clear()     
            matchpos={}   
            
            readid = i
#            print "@",i
            
            # setup automata to the initial state
            state = self._states
            table = &(state.a)
            for j in range(readsize4):
                nucs = <unsigned char*>&(expanded8bitsnuc[nuc4[j]])
                for k in range(4):
                    letter = nucs[k]
                    nstate = table[letter]
                    pmatch = nstate.match
                    while (pmatch!=NULL):
                        pid = pmatch.protid
                        if pid < 0 :
                            pid += mid
                        wordcount.set(pid,pmatch.position)
                        matchpos[pid]=min(matchpos.get(pid,65535),pmatch.position)
                        pmatch = pmatch.next
                    state = nstate
                    table = &(state.a)
                    
            wordmax=0
            protidmax=0
            framemax=0
            
            count = wordcount.counter()
            
            for k in range(1,self._maxseqid+1):
                pid = k 
                
                wc[1]=count[pid]
                rp[1]=matchpos.get(pid,65535)                
                #memcpy(<void*>(wc+3),<void*>(count+pid),3*sizeof(size_t))
                
                pid = mid - pid 
                 
                wc[0]=count[pid]
                rp[0]=matchpos.get(pid,65535)
                
                # memcpy(<void*>(wc),<void*>(count+pid),3*sizeof(size_t))
                
                wct = wc[0] + wc[1]
                if wc[0] > wc[1]:
                    phase=-1
                    wcmax=wc[0]
                    loc=rp[0]
                else:
                    phase=1
                    wcmax=wc[1]
                    loc=rp[1]
                

                if (wcmax >=minmatch):
                    wordmax = wcmax
                    protidmax=k
                    framemax= phase 
                    locmax=loc

                
            nbreads=1
            nuc4bis=nuc4 + recordsize
            i+=1

            if (progress):
                pb(i)

            while (i< readcount and 
                   samereads(nuc4, nuc4bis, readsize64)):
                nbreads+=1
                nuc4bis+= recordsize
                i+=1
                
#            print "Best match : %d -> %d (%d)" % (protidmax,wordmax,nbreads) 

            nuc4 = nuc4bis
            
            if protidmax>0 and nbreads >= covmin:
                if framemax < 0:
                    readid = -readid - 1
                else:
                    readid+=1 
                    
                plpos = PyDict_GetItem(results,PyInt_FromLong(protidmax))
                if plpos==NULL:
                    lpos = []
                    PyDict_SetItem(results,PyInt_FromLong(protidmax),lpos)
                else:
                    lpos = <object>plpos
                lpos.append((readid,wordmax,nbreads,framemax,0,locmax))
                
                
        ks = list(results.keys())

        for k in ks:
            results[self._rseqid[k]]=results[k]
            del results[k]
        

        return results
                    