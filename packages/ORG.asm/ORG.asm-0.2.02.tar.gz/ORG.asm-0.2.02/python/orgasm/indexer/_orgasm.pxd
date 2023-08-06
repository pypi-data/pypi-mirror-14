# cython: language_level=3
from .fakereads cimport FakeReads
from cpython cimport array as c_array

cdef extern from *:
    ctypedef char* const_char_p "const char*"

cdef extern from "inttypes.h":
    ctypedef int int32_t
    ctypedef unsigned int uint32_t


cdef extern from "string.h":
    cdef int  strncmp(const_char_p s1, const_char_p s2, size_t n)
    
cdef extern from "orgasm.h":
    ctypedef struct buffer_t:
        size_t         readSize     # Size of one read in base pair
        size_t         recordSize   # Size in bytes of one compressed read
        char*          records      # the start of the first record [0].
        size_t         readCount    # count of reads. One pair of reads counts for 2
        uint32_t*      order1       # a pointer used to point on a int array indicating an order
                                    # over the records. @IndentOk
        uint32_t*      order2       # a pointer used to point on a int array indicating an order
                                    # over the records.
        uint32_t*      complement

    ctypedef unsigned char* pnuc

cdef class Index:

    cdef buffer_t* _index
    cdef FakeReads _fakes

    cpdef bint contains(self, bytes word)
    cpdef int count(self, bytes word)
    cpdef int len(self)
    cpdef bytes getRead(self, int32_t readid, int32_t begin, int32_t length)
    cpdef dict getExtensions(self, bytes word)
    cpdef int getReadSize(self)
    cpdef tuple getReadIds(self, bytes seq)
    cpdef tuple getIds(self, int32_t id)
    cpdef int32_t getPairedRead(self, int32_t id)
    cpdef tuple normalizedPairedEndsReads(self, int32_t id)
    cpdef dict lookForSeeds(self, dict sequences, 
                            int kup=?, int mincov=?,
                            float identity=?,
                            object logger=?)
    cdef c_array.array lookForString(self, bytes word)

    cpdef dict checkedExtensions(self, bytes  probe,
                                       tuple  adapters5=?,
                                       tuple  adapters3=?,
                                       int    minread=?,
                                       double minratio=?,
                                       int    mincov=?,
                                       int    minoverlap=?,
                                       int    extlength=?,
                                       bint   lowfilter=?,
                                       object restrict=?,
                                       bint   exact=?)
