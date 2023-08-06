# cython: language_level=3

cpdef dict hashSeq(bytes seq, size_t kmer=?)
cpdef tuple cmpHash(dict h1,dict h2, size_t delta=?)
