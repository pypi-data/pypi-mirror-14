# cython: language_level=3

from cpython.bytes cimport PyBytes_FromStringAndSize, PyBytes_GET_SIZE
from collections import Counter

#                   "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cdef char* __COMP = "T-G---C------------A------"

cdef int _reverseComplement(char* seq, size_t length):
    """
    Internal function computing the reverse complement sequence
    of a DNA sequence in place.
    """
    cdef char   tmp
    cdef char*  end = seq + length -1
    
    while seq <= end:
        tmp = end[0]
        end[0] = __COMP[(seq[0] & (~32)) - 65]
        seq[0] = __COMP[(tmp & (~32)) - 65]
        seq+=1
        end-=1 
        
    return 0
    
cpdef bytes reverseComplement(bytes seq):
    """
    Computes the reverse complement sequence of a DNA sequence
    composed only of acgt. No check is done for efficiency 
    purpose so be careful to the input sequence.
    
    :param seq: the sequence to revert-compelent expressed as
                a serie of acgt in upper or lower case
    :type  seq: a bytes instance
    
    :return: the reverse-complemented sequence in upper case
    :rtype:  a bytes instance
    """
    cdef bytes  comp 
    cdef char*  ccomp= seq
    cdef size_t lcomp= PyBytes_GET_SIZE(seq)
    
    comp = PyBytes_FromStringAndSize(ccomp,lcomp)
    ccomp= comp
    
    _reverseComplement(ccomp,lcomp)
    
    return comp

cpdef bint isDNA(bytes seq):
    cdef set c = set([x for x in seq.upper()])
    return len(c)==4


cdef dict codon = {}
cdef int i

ncbieaa="FFLLSSSSYYQQCCGWLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
Base1  ="TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG"
Base2  ="TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG"
Base3  ="TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG"

for i in range(len(ncbieaa)):
    codon[Base1[i]+Base2[i]+Base3[i]]=ncbieaa[i]
    
cpdef tuple translate3(bytes seq): 
    cdef int i                               # @DuplicatedSignature
    cdef list prot0=[]
    cdef list prot1=[]
    cdef list prot2=[]
    
    
    for i in range(len(seq)-3):
        aa = codon[seq[i:(i+3)].upper()]
        p = i % 3
        if p==0:
            prot0.append(aa)
        elif p==1:
            prot1.append(aa)
        else:
            prot2.append(aa)
            
    return (b''.join(prot0),
            b''.join(prot1),
            b''.join(prot2)
            )
            