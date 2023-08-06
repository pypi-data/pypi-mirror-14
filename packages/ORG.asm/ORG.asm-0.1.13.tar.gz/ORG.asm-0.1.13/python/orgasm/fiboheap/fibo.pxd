# cython: language_level=3

cdef extern from "fibo.h":
    ctypedef struct FiboNode:
        pass
    
    ctypedef struct FiboTree:
        pass
    
    ctypedef FiboNode* const_FiboNode_ptr_const "const FiboNode * const"
    ctypedef FiboNode* const_FiboNode_ptr "const FiboNode *"
    ctypedef FiboTree* const_FiboTree_ptr "const FiboTree *"
    
    int fiboTreeInit(const_FiboTree_ptr tree, int (*) (const_FiboNode_ptr_const node1,const_FiboNode_ptr_const node2))
    void fiboTreeExit(const_FiboTree_ptr tree)
    void fiboTreeFree(const_FiboTree_ptr tree)
    FiboNode *fiboTreeConsolidate (const_FiboTree_ptr tree)
    void fiboTreeAdd(const_FiboTree_ptr tree, const_FiboNode_ptr node)
    void fiboTreeDel(const_FiboTree_ptr tree, const_FiboNode_ptr node)
    FiboNode *fiboTreeMin(const_FiboTree_ptr tree)
    int fiboTreeCheck(const_FiboTree_ptr tree)
