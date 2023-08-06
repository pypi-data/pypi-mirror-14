# cython: language_level=3

cdef import from "stdlib.h":
    void* malloc(int size)  except NULL
    void* realloc(void* chunk,int size)  except NULL
    void free(void* chunk)
    
cdef import from "string.h":
    void bzero(void *s, size_t n)
    void memset(void* chunk,int car,int length)
    void memcpy(void* s1, void* s2, int n)
    
cdef struct AlignCell :
    int score
    int   path 
    
cdef struct AlignMatrix :
    AlignCell*  matrix
    int         msize
    int         vsize
    int         hsize
   


cdef AlignMatrix* allocateMatrix(int hsize, int vsize,AlignMatrix *matrix=?)

cdef void freeMatrix(AlignMatrix* matrix)

cdef void resetMatrix(AlignMatrix* matrix)

cdef struct alignPath:
    long length
    long buffsize
    long *path
    
cdef alignPath* allocatePath(long l1,long l2,alignPath* path=?)

cdef void reversePath(alignPath* path)


cdef void freePath(alignPath* path)



cdef class EndGapFree:
    cdef AlignMatrix* matrix

    cdef bytes horizontalSeq 
    cdef bytes verticalSeq
    
    cdef char* hSeq
    cdef char* vSeq
    cdef long  lhSeq
    cdef long  lvSeq
    cdef alignPath*     path

    cdef object alignment
    
    cdef bint sequenceChanged
    cdef bint matchScore(self,int h, int v)
    
    cdef int allocate(self) except -1
    cdef long doAlignment(self) except? 0
    cdef void reset(self)
    cdef inline int index(self, int x, int y)
    cdef void backtrack(self)
    cdef void clean(self)

