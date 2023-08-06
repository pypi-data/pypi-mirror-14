# cython: language_level=3

cdef int _reverseComplement(char* seq, size_t length)
cpdef bytes reverseComplement(bytes seq)
cpdef bint isDNA(bytes seq)
cpdef tuple translate3(bytes seq)
