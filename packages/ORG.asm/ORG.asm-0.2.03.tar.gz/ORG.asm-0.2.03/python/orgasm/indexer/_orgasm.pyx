# cython: language_level=3
from asyncio.log import logger
cimport cython

from ._orgasm cimport *
from cpython.bytes cimport PyBytes_Size,PyBytes_AsString,PyBytes_GET_SIZE

from cpython.dict cimport PyDict_Merge,PyDict_GetItem
from cpython.list cimport PyList_GET_ITEM,PyList_SetItem,PyList_Append
from cpython.int  cimport PyInt_AS_LONG,PyInt_FromLong

from array import array

from orgasm.backtranslate._ahocorasick cimport *
from orgasm.utils.dna cimport isDNA
#from time import time

from posix.time cimport timeval,gettimeofday

import sys

cdef bint adapter(bytes probe, tuple adapterSeq5, tuple adapterSeq3):
    return ( any([probe.startswith(y) for y in adapterSeq5]) or 
             any([probe.endswith(y) for y in adapterSeq3]) )


cdef extern from "stdlib.h":
    ctypedef unsigned int size_t
    int32_t abs(int32_t i)

cdef extern from "math.h":
    double log10(double x)
    double ceil(double x)

cdef extern from "orgasm.h":
    void freeBuffer(buffer_t *buffer)

    buffer_t *loadIndexedReads(char *indexname)

    int32_t lookForString(buffer_t *buffer, char *key, size_t length, int32_t* endoflist)
    int32_t fastLookForString(buffer_t *buffer, char *key, size_t length, int32_t* fcount, int32_t* rcount, int32_t* fpos, int32_t* rpos)
    int32_t nextRead(buffer_t *buffer, int32_t current, size_t length, int32_t* endoflist)
    int32_t lookForReadsIds(buffer_t *buffer, int32_t key, int32_t* endoflist)
    int32_t nextReadIds(buffer_t *buffer, int32_t current, int32_t* endoflist)
    char *getRead(buffer_t *buffer, int32_t recordid, uint32_t begin, int32_t length, char *dest)

cdef bint lowcomplexity(bytes s):
    """
    Returns True if the word s is an homopolymer, an homo-dimer
    or an homo-trimer

    @param s: the string to test
    @type s: bytes

    @return True if s is an homopolymer, an homedimer
            or an homotrimer, False otherwise
    @rtype: bool
    """
    cdef int ls=PyBytes_GET_SIZE(s)
    cdef char* ps = PyBytes_AsString(s)
    cdef bint r = (strncmp(ps,ps+2,ls - 2) * strncmp(ps,ps+3,ls - 3)) == 0
    return r 
#    return s[0:-2] == s[2:] or s[0:-3] == s[3:]

cdef double time():
    cdef double  seconds
    cdef double  usec
    cdef timeval tv
    gettimeofday (&tv, NULL);
    seconds = tv.tv_sec
    usec    = tv.tv_usec / 1000000.
    return seconds + usec 
    
cdef class Index:

    def __init__(self,str name):
        cdef int minfake

        self._index=loadIndexedReads(bytes(name,'latin1'))
        minfake = <int>(10**ceil(log10(self._index.readCount))) + 1
        self._fakes=FakeReads(minfake,self._index.readSize)

    cpdef bint contains(self, bytes word):
        cdef int32_t endoflist
        cdef size_t  lword = PyBytes_Size(word)

        lookForString(self._index,word,lword,&endoflist)

        return endoflist==0

    cpdef int count(self, bytes word):
        return len(self.lookForString(word))

    cpdef int len(self):
        return self._index.readCount

    cpdef bytes getRead(self, int32_t readid, int32_t begin, int32_t length):
        """
        getRead methods allows to access to the the sequence of the reads stored in the
        index. The read id is include in the interval [-n,-1] U [1,n] with n the count
        of read in the index. the read 0 does not exist.
        """
        cdef char buffer[500]
        cdef bytes seq

        assert begin < self._index.readSize,"Begin must be smaller than read size"
        assert begin+length <= self._index.readSize,"Begin+Length must be smaller than read size"

        if self._fakes.isFake(readid):
            seq = self._fakes.getRead(readid,begin,length)
        elif readid==0 or abs(readid)>self._index.readCount:
            raise IndexError(readid)
        else:
            seq=getRead(self._index, readid, begin, length, buffer)

        return seq

    cpdef dict getExtensions(self, bytes word):
        cdef dict rep
        cdef int32_t readid                                 # @DuplicatedSignature
        cdef size_t  lword = PyBytes_Size(word)                      # @DuplicatedSignature
        cdef size_t  lext  = self._index.readSize - lword
        cdef bytes e
        cdef list  data
        cdef c_array.array w
        cdef long[:] cw
        cdef size_t  lw
        cdef size_t  i
        cdef double ellapsed = time()
        cdef PyObject *pdata
        cdef object o
        cdef list ids
        cdef int nread

        rep = {}
        
        w = self.lookForString(word)
        lw = len(w)
        cw = w
        
        for i in range(lw):
            readid = cw[i]
            # assert abs(readid) < self._index.readCount
            e = self.getRead(readid,lword, lext)
            pdata = PyDict_GetItem(rep,e)
            if pdata==NULL:
                data=[0,[]]
                rep[e]=data
            else:
                data= <list> pdata

            data[0]+=1

            pdata = PyList_GET_ITEM(data,1)
            ids = <list> pdata
            PyList_Append(ids,PyInt_FromLong(readid))
            
        ellapsed = time()  - ellapsed
        
        if ellapsed > 0.5:
            print("\nWarning too long getExtension (%4.2fs): %s -> %d matches\n" % (ellapsed,word,len(w)),file=sys.stderr)

        return rep

    cpdef dict checkedExtensions(self, bytes probe,
                                       tuple adapters5=(),
                                       tuple adapters3=(),
                                       int minread=20,
                                       double minratio=0.1,
                                       int mincov=1,
                                       int minoverlap=40,
                                       int extlength=1,
                                       bint lowfilter=True,
                                       object restrict=None,
                                       bint exact=True):
        '''
        :param probe: The sequence used as prefix in the selection
        :type probe:  bytes
        :param minread: the minimum count of read to consider
        :type minread:  int
        :param minratio: minimum ratio between occurrences of an extension
                         and the occurrences of the most frequent extension
                         to keep it.
        :type minratio:  float [0,1]
        :param mincov:   minimum occurrences of an extension to keep it
        :type mincov:    int
        :param minoverlap: minimum length of the probe usable
        :type minoverlap: int
        '''

        cdef dict  ext       = {}
        cdef dict  lext
        cdef int   covmax    = 0
        cdef int   readcount = 0
        cdef list  e,rs,ks,rk
        cdef list  allexts
        cdef dict  extcount = {}
        cdef bytes k
        cdef int   x
        cdef int   r,rn,rsize
        cdef bytes oriprobe

        oriprobe = probe
        
            
        
        while ( not (     (    lowcomplexity(probe) 
                            or adapter(probe, adapters5,adapters3)
                          ) 
                      and      lowfilter
                    ) 
                and PyBytes_Size(probe) >= minoverlap   
                and (    readcount < minread 
                      or exact
                    )
              ):
            
            trueoverlap = len(probe)
            lext = self.getExtensions(probe)
                        
            if restrict is not None:
                ks = list(lext.keys())
                for k in ks:
                    rs=lext[k][1]
                    rk=[]
                    for r in rs:
                        if r in restrict:
                            rk.append(r)
                        else:
                            rn = self.getPairedRead(r)
                            if rn:
                                rn = self.getIds(rn)[0]
                                if rn in restrict:
                                    rk.append(r)
                            
                    if rk:
                        lext[k][1]=rk
                    else:
                        del lext[k]
                                    
#             if restrict is not None:
#                 ks = lext.keys()
#                 for k in ks:
#                     rs=lext[k][1]
#                     rk=[]
#                     for r in rs:
#                         rn = self.getPairedRead(r)
#                         if rn:
#                             rn = self.getIds(rn)[0]
#                             if rn in restrict:
#                                 rk.append(r)
#                     if rk:
#                         lext[k][1]=rk
#                     else:
#                         del lext[k]

            if lext:
                for e in lext.itervalues():
                    readcount+=e[0]
                ext.update(lext)
                
            probe=probe[1:]
            
            
        ##-------------------END OF THE WHILE LOOP ----------------------##

        if readcount < minread:
            ext={}
        elif ext:
            allexts = [(k[0:extlength],ext[k][0]) for k in ext.keys()]
            extcount= {}
            for k,x in allexts:
                extcount[k]=extcount.get(k,0)+x
                
            rsize = self.getReadSize()
            
            # Evaluate the true coverage according the actual overlap
            for k,x in extcount.items():
                extcount[k]=x * rsize // (rsize - trueoverlap)

            covmax = max(extcount.values())

            it = list(extcount.items())

            for k,x in it:
                if (   x < mincov 
                    or <double>x/<double>covmax < minratio):
                    del extcount[k]
                else:
                    data = ext.get(k,(0,[]))[1]
                    if not data:
                        data=list(self.getReadIds(oriprobe+k)[2])

                    extcount[k]=(extcount[k],data)


        return extcount


    cpdef int getReadSize(self):
        return self._index.readSize

    cpdef tuple getReadIds(self, bytes seq):

        cdef c_array.array x
        cdef int  y
        cdef int  t

        assert len(seq)==self._index.readSize,"seq must have the same length than reads"

        x = self.lookForString(seq)

        if x:
            t = len(self)+1

            for y in x:
                if abs(y) < abs(t):
                    t = y
            y = len(x)
        else:
            f = self._fakes.getReadIds(seq)
            return f 

        return (t,y,set(x))

    cpdef int32_t getPairedRead(self, int32_t id):
        cdef int32_t iid = abs(id)
        cdef int32_t pid

        if iid > self._index.readCount:
            pid = 0
        else:
            pid = self._index.order2[iid-1] + 1

        if id > 0:
            pid = - pid

        return pid

    cpdef tuple normalizedPairedEndsReads(self, int32_t id):
        '''
        Returns for a read id the normalized set of paired reads corresponting to it.

        :param id: the read id
        @return: a tuple of two elements
                    - an integer value : the normalized id
                    - a list of integers : the normalized ids of the paired reads
        '''
        cdef int32_t nid
        cdef int32_t n
        cdef set synomymes
        cdef int32_t i
        cdef list paired
        cdef tuple k
        cdef int idsign = 1 if id > 0 else -1 
        
        nid,n,synomymes = self.getIds(id)
          
        if id not in synomymes:
            nid=-nid
            synomymes=set([-i for i in synomymes])

        goodsyno = [x for x in synomymes if x * idsign > 0]

        paired = [self.getPairedRead(i) for i in goodsyno]
        
        paired = [(j,self.getIds(j)) for j in paired]
        paired = [k[0] if j in k[2] else -k[0] for j,k in paired]
        return nid,paired


    cpdef dict lookForSeeds(self, dict sequences, 
                            int kup=-1, int mincov=1,
                            float identity=0.5,
                            object logger=None):

        cdef AhoCorasick patterns
        cdef dict matches
        cdef str k   
        cdef bint  nuc   
        
        nuc = all([isDNA(sequences[k]) for k in sequences])
            
        if nuc:
            if logger is not None:
                logger.info('Matching against nucleic probes')
            patterns = NucAhoCorasick()
            kup = 12 if kup < 0 else kup
        else:
            if logger is not None:
                logger.info('Matching against protein probes')
            patterns = ProtAhoCorasick()
            kup = 4 if kup < 0 else kup

        for k in sequences:
            patterns.addSequence(sequences[k],k,kup)

        
        patterns.finalize()
                
        #minmatch = 50 if nuc else 15
        minmatch = int((self.getReadSize() // (1 if nuc else 3)) * identity)
        logger.info('Minimum word matches = %d ' % minmatch)
        
        matches = patterns.scanIndex(self,minmatch,-1,mincov)

        return matches



    cpdef tuple getIds(self, int32_t id):
        cdef int32_t endoflist                                      # @DuplicatedSignature
        cdef int32_t readid                                         # @DuplicatedSignature
        cdef list    reads = []
        cdef int  y                                                 # @DuplicatedSignature
        cdef int  x
        cdef int  t                                                 # @DuplicatedSignature

        if id==0:
            raise IndexError(id)

        if self._fakes.isFake(id):
            return self._fakes.getIds(id)

        y = abs(id)
        
        if y > self._index.readCount:
            raise IndexError("%d (Maximum id is %d)" % (id,self._index.readCount))

        readid = lookForReadsIds(self._index,id,&endoflist)

        while(endoflist==0):
            reads.append(readid)
            readid = nextReadIds(self._index,readid,&endoflist)

        if reads:
            t = len(self)+1

            for y in reads:
                if abs(y) < abs(t):
                    t = y

            if t < 0:
                reads = [-x for x in reads]
                t = -t

        return (t,len(reads),set(reads))


    def __dealloc__(self):
        freeBuffer(self._index)

    def __contains__(self, bytes word):
        return self.contains(word)
    
    @cython.boundscheck(False)
    cdef c_array.array lookForString(self, bytes word):
        cdef int32_t fpos                                       # @DuplicatedSignature
        cdef int32_t rpos                                       # @DuplicatedSignature
        cdef int32_t fcount                                     # @DuplicatedSignature
        cdef int32_t rcount                                     # @DuplicatedSignature
        cdef int32_t count                                      # @DuplicatedSignature
        cdef int32_t readid                                     # @DuplicatedSignature
        cdef size_t  lword = len(word)                          # @DuplicatedSignature
        cdef c_array.array readids = array('l', [0])
        cdef long[:] creadids

        count  = fastLookForString(self._index,word,lword,&fcount,&rcount,&fpos,&rpos)
        c_array.resize(readids,count)
        creadids=readids
#        print fcount,rcount,fpos,rpos
#        print count
        for readid in range(count):
            if readid < fcount:
                fpos+=1
                creadids[readid]=fpos
            else:
                creadids[readid]=-(<int32_t>self._index.order1[rpos])-1
                rpos+=1
                
#         readids=list(range(fpos+1,fpos+count+1))
#         for readid in range(fcount,count):
#             readids[readid]=-(<int32_t>self._index.order1[readid-fcount+rpos])-1 
            
#        print readids
        
        return readids

    def __getitem__(self, bytes word):
        return self.lookForString(word)
    

    def __len__(self):
        return self.len()

    def checkReverseOrder(self):
        conv = {'A':'0','C':'1','T':'2','G':'3'}
        from orgasm.utils.dna import reverseComplement
        olds=" "
        for i in range(len(self)):
            j = self._index.order1[i] + 1
            s = "".join(conv[x] for x in reverseComplement(self.getRead(j,0,self.getReadSize())))
            if olds > s:
                print(i,olds,s)
                raise AssertionError
            else:
                olds=s



    property fakes:

        "An direct access to the fake reads."

        def __get__(self):
            return self._fakes









