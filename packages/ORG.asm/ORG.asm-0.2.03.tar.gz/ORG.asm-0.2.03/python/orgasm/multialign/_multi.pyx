# cython: language_level=3

from collections import Counter


from orgasm.apps.progress cimport ProgressBar 
from ._dynamic cimport EndGapFree
from orgasm.indexer._orgasm cimport Index
from collections import Counter

cpdef dict hashSeq(bytes seq, size_t kmer=12):
    '''
    Build a hash table of the kmer constituing the sequence seq
    :param seq: a dna sequence, supposed to be in uppercase
    :type seq: bytes
    :param kmer: the size of the considered kmer
    :type kmer: int
    :return: an associative array containing the hash table with kmer as key and an array
             of integer positions as value
    :rtype: a dict instance indexed by bytes and containing list of int
    '''
    
    cdef size_t lseq = len(seq)
    cdef dict h = {}
    cdef size_t i
    cdef bytes  w 
    cdef list   p 
    
    for i in range(lseq-kmer+1):
        w = seq[i:(i+kmer)]
        p = h.get(w,[])
        p.append(i)
        h[w]=p
    return h

cpdef tuple cmpHash(dict h1,dict h2, size_t delta=2):
    '''
    Compare two hash tables as build by the hashSeq function.

    :param h1: the first hash table
    :type h1: a dict instance indexed by bytes and containing list of int
    :param h2: the second hash table
    :type h2: a dict instance indexed by bytes and containing list of int
    :param delta: delta around the main diagonal considered to compute the score
    :type delta: int
    :return: the shift corresponding to the main diagonal and the corresponding score
    :rtype: a tuple of two int 
    '''
    
    cdef set k1
    cdef set k2
    cdef set kc
    cdef bytes k 
    cdef list p1
    cdef list p2
    cdef int i
    cdef int j
    cdef int shift
    cdef int score
    
    k1 = set(h1.keys())
    k2 = set(h2.keys())
    kc = k1 & k2
    stat = Counter()
    for k in kc:
        p1 = h1[k]
        p2 = h2[k]
        stat.update([i - j for i in p1 for j in p2])
    mstat = stat.most_common()
    if mstat:
        shift = mstat[0][0]
        
        score = 0
        for i in range(-delta+shift,shift+delta+1):
            score+=stat.get(i,0)
        mstat=(shift,score)
    else:
        mstat =(0,0)
    return mstat

cdef tuple alignSequence(bytes seq1, bytes seq2,
                  dict hash1=None,dict hash2=None,
                  size_t kmer=12,size_t delta=2,
                  int smin=10,EndGapFree align=None):

    cdef int shift                                  # @DuplicatedSignature
    cdef int score                                  # @DuplicatedSignature
    cdef size_t lseq1
    cdef size_t lseq2
    cdef bint direction    
    cdef bytes subseq1
    cdef bytes subseq2
    cdef tuple ali
    cdef dict gaps1
    cdef dict gaps2
    cdef int p
    cdef int n
    cdef int g 
    
    if align is None:
        align = EndGapFree()
    if hash1 is None:
        hash1=hashSeq(seq1, kmer)
    if hash2 is None:
        hash2=hashSeq(seq2, kmer)
        
    shift,score = cmpHash(hash1, hash2, delta)
    
    if score > smin:
        lseq1=len(seq1)
        lseq2=len(seq2)
        if shift < 0:
            direction=True
            subseq1 = seq1[0:shift]
            subseq2 = seq2[shift:]
            shift=-shift
            if subseq1==subseq2:
                ali = ([[0,shift],[lseq1,0]],[[lseq2,shift]])
            else:
                align.seqA=seq1
                align.seqB=seq2
                ali = align()
                shift = ali[0][0][1]
        else:
            direction=False
            subseq1 = seq1[shift:]
            subseq2 = seq2[0:lseq2-shift]
            if subseq1==subseq2:
                ali = ([[0,shift],[lseq2,0]],[[lseq1,shift]])
            else:
                align.seqA=seq2
                align.seqB=seq1
                ali = align()
                
        ali[0][-1][1]=0
        ali[1][-1][1]=0
        
        p=0
        gaps1={0:0}
        for n,g in ali[0]:
            p+=n
            if g > 0:
                gaps1[p]=g 
        p=0
        gaps2={0:0}
        for n,g in ali[1]:
            p+=n
            if g > 0:
                gaps2[p]=g 
            
    else:
        direction=True
        shift=0
        score=0
        gaps1=None
        gaps2=None

    # direction is True if seq2 starts before seq1
    return direction,score,gaps1,gaps2
    
def skey(tuple x): 
    return x[0]

cdef list alignReads(readids,Index index,size_t kmer=12,int smin=10,size_t delta=2):
    cdef EndGapFree align = EndGapFree()

    cdef size_t rsize = index.getReadSize()
    cdef size_t nseq
    cdef list seqs
    cdef list hashes
    cdef dict unique = {}
    
    cdef list scores = []
    cdef size_t nali
    cdef size_t pos  = 1
    cdef size_t h1
    cdef size_t h2
    cdef bytes s
    cdef int j                                      # @DuplicatedSignature
    cdef ProgressBar pb
    
    # We dereplicate the sequences
    for j in readids:
        s = index.getRead(j,0,rsize)
        l = unique.get(s,[])
        l.append(j)
        unique[s]=l
        
    seqs = list(unique)
#    nseq   = len(readids)
    nseq   = len(seqs)
    nali = nseq * (nseq-1) // 2
    hashes =[hashSeq(s,kmer) for s in seqs]
    
    pb = ProgressBar(nali,head="Pairwise alignment %6d x %6d " % (0,0))
    
    for h1 in range(nseq):
        for h2 in range(h1+1,nseq):
            pb.head="Pairwise alignment %6d x %6d " % (h1,h2)
            pb(pos)
            pos+=1
            
            ali = alignSequence(seqs[h1],seqs[h2],
                                hashes[h1],hashes[h2], 
                                kmer, delta, smin, align)
            if ali[1] > smin:      # if the alignment score is greater than smin
                for j in unique[seqs[h1]]:
                    for k in unique[seqs[h2]]:
                        # if seq2 starts before seq1 we swap sequences 
                        if not ali[0]:
                            k,j=j,k 
                        scores.append((ali[1],
                                      (j,ali[2]),
                                      (k,ali[3]))
                                      )
        
    scores.sort(key=skey,reverse=True)
    
    return scores



cdef dict newGaps(newali,oldali):
    cdef dict delta={}
    cdef int d 
    
    for p in newali:
        d = newali[p]-oldali.get(p,0)
        if d > 0:
            delta[p]=d 
    return delta
    
def readPos2Alignment(ali,read,pos):
    ref  = ali[read]
    apos = sum(x[1] for x in ref.iteritems() if x[0] <= pos) + pos
    return apos
    
def alignPos2Read(ali,read,pos):
    ref  = ali[read]
    posgap = list(ref.items())
    posgap.sort(key=lambda x:x[0])        
    
    b = sum(posgap[0])
    bornes = [(b,0)]
    
    for i,j in posgap:
        if i > 0:
            b+=i 
            bornes.append((b,bornes[-1][1]))
            b+=j
            bornes.append((b,i))

#    print bornes
    
    if pos < bornes[0][0]:
#        tag = "*"
        rpos=0
    else:
        i=0
        lb = len(bornes)
        while i < lb and pos > bornes[i][0]:
            i+=1
            
        if i == lb:
#            tag = "@"
            rpos = pos - bornes[-1][0] + bornes[-1][1]
        else:
            isnuc = i & 1
            if isnuc:
#                tag = "+"
                rpos = pos - bornes[i-1][0] + bornes[i][1]
            else:
#                tag = "-"
                rpos = bornes[i][1] 
            
    return rpos
    
def applyGaps(key,gaps,ali,rsize):
    
    
    if gaps:
#         time.sleep(1)
#         print key,gaps,ali,rsize
        for pos,length in gaps.iteritems():
            pali = readPos2Alignment(ali, key, pos)
            for read in ali:
                pread = alignPos2Read(ali, read, pali)
                if pread < rsize:
                    ali[read][pread]=ali[read].get(pread,0)+length
#        print ">>>",ali
    return ali
                    
def mergeAlignments(common, ali1,ali2,rsize):
    r1 = ali1[common]
    r2 = ali2[common]
    
    lr1 = len(r1)
    lr2 = len(r2)
    
    if lr1 > lr2:
        r1,r2 = r2,r1
        ali1,ali2 = ali2,ali1
        
    delta = r2[0] - r1[0]
        
    for r in ali1.itervalues():
        r[0]+=delta 
        
    ngap1 = newGaps(r1, r2)
    ngap2 = newGaps(r2, r1)
    

    applyGaps(common,ngap1,ali2,rsize)
    applyGaps(common,ngap2,ali1,rsize)
    
    ali2.update(ali1)

    return ali2
    
    
    
    

def multiAlignReads(readids,index,kmer=12,smin=10,delta=2):
    readids = list(set(readids))
    cdef list scores=alignReads(readids,index,kmer,smin,delta)
    cdef int  rsize = index.getReadSize()
    
    cdef dict alignment={}
    
    for (score,(r1,ali1),(r2,ali2)) in scores:
        partial1 = [x for x in alignment.items() if r1 in x[0]]
        partial2 = [x for x in alignment.items() if r2 in x[0]]

        if not partial1 or (partial1 and not r2 in partial1[0][0]):
            # the two reads are not already in the same alignment
            if partial1:
                del alignment[partial1[0][0]]
                partial1 = partial1[0][1]
                tmp      = {r1:ali1, r2:ali2}
    #            print r1, partial1, tmp
                partial1 = mergeAlignments(r1, partial1, tmp, rsize)
            else:
                partial1 = {r1:ali1, r2:ali2}
                
    
            if partial2:
                del alignment[partial2[0][0]]
                partial2 = partial2[0][1]
                merged   = mergeAlignments(r2, partial1, partial2, rsize)
            else:
                merged   = partial1
                
            alignment[frozenset(merged)]=merged
        
    for k in alignment:
        al = alignment[k]
        minshift = min(i[0] for i in al.values())
        for i in al:
            al[i][0]=al[i][0]-minshift
    
    return list(alignment.values())

def alignment2bytes(ali,index):
    cdef bytes seq
    cdef int   i=0
    cdef int rsize= index.getReadSize()
    cdef list res=[] 
    cdef int r 
    cdef list gaps
    cdef list aseq
    cdef int  pos,length 
    
    for r in ali:
        seq = index.getRead(r,0,rsize)
        gaps = list(ali[r].items())
        gaps.sort(key=lambda g:g[0])
        aseql=[]
        for pos,length in gaps:
            if pos>0:
                aseql.append(seq[i:pos])
                aseql.append(b'-'*length)
            else:
                aseql.append(b'+'*length)                
            i=pos
        aseql.append(seq[i:rsize])
#        print ali[r],''.join(aseql)
        res.append(b''.join(aseql))
        res.sort()      

    return res


def consensus(aln,Index index,int covmin=5):
    cdef int pos=0
    cdef int ii,j
    cdef tuple i
    cdef list seql
    cdef bytes seq
    cdef int   lseq
    cdef int lali
    cdef list coverage

    res = alignment2bytes(aln,index)
    lali = max(len(i) for i in res)
    seql = [Counter([l for l in [s[pos:pos+1] for s in res] 
                     if l and l in b'-ACGT']).most_common()[0] 
            for pos in range(lali)]
    seql = [i for i in seql if i[0]!=b'-']
    coverage = [i[1] for i in seql]
    seq = b''.join([i[0] for i in seql])
    ii=0
    lseq=len(seq)
    while ii < lseq and coverage[ii] < covmin:
        ii+=1
    j=len(coverage)-1
    while j >= 0 and coverage[j] < covmin:
        j-=1
        
    if ii < j:
        seq = seq[ii:j+1]
    else:
        seq = b""
    return seq        
     
