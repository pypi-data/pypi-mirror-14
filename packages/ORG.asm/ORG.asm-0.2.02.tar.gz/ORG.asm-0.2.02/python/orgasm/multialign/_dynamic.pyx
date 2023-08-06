# cython: language_level=3
'''
Created on 14 sept. 2009

@author: coissac
'''
######
#
# Import standard memory management function to improve
# efficiency of the alignment code
#
#

from ._dynamic cimport * 
    
cdef AlignMatrix* allocateMatrix(int hsize, int vsize,AlignMatrix *matrix=NULL):
    
    cdef int msize
    
    vsize+=1
    hsize+=1
    
    if matrix is NULL:
        matrix = <AlignMatrix*>malloc(sizeof(AlignMatrix))
        matrix.msize=0
        matrix.matrix=NULL
        
    msize = hsize * vsize 
    if msize > matrix.msize:
        matrix.msize = msize
        matrix.matrix = <AlignCell*>realloc(matrix.matrix, msize * sizeof(AlignCell))
        
    return matrix

cdef void freeMatrix(AlignMatrix* matrix):
    if matrix is not NULL:
        if matrix.matrix is not NULL:
            free(matrix.matrix)
        free(matrix)
        
cdef void resetMatrix(AlignMatrix* matrix):
    if matrix is not NULL:
        if matrix.matrix is not NULL:
            bzero(<void*>matrix.matrix, matrix.msize * sizeof(AlignCell))
     
    
cdef alignPath* allocatePath(long l1,long l2,alignPath* path=NULL):
    cdef long length=l1+l2
    
    if path is NULL:
        path = <alignPath*>malloc(sizeof(alignPath))
        path.length=0
        path.buffsize=0
        path.path=NULL
        
    if length > path.buffsize:
        path.buffsize=length
        path.path=<long*>realloc(path.path,sizeof(long)*length)
        
    path.length=0
    
    return path

cdef void reversePath(alignPath* path):
        cdef long i
        cdef long j
        
        j=path.length
        for i in range(path.length//2):
            j-=1
            path.path[i],path.path[j]=path.path[j],path.path[i]

cdef void freePath(alignPath* path):
    if path is not NULL:
        if path.path is not NULL:
            free(<void*>path.path)
        free(<void*>path)
  
    
cdef class EndGapFree:

    def __init__(self):
        self.sequenceChanged=True

        self.matrix=NULL
        self.hSeq=NULL
        self.vSeq=NULL
        self.path=NULL
        
        self.horizontalSeq=None
        self.verticalSeq=None
        
    cdef int allocate(self) except -1:
        
        assert self.horizontalSeq is not None,'Sequence A must be set'
        assert self.verticalSeq is not None,'Sequence B must be set'
        
        cdef long lenH=len(self.horizontalSeq)
        cdef long lenV=len(self.verticalSeq)

        self.matrix=allocateMatrix(lenH,lenV,self.matrix)
        return 0


    cdef bint matchScore(self,int h, int v):
        return self.hSeq[h-1]==self.vSeq[v-1]
        
    cdef inline int index(self, int x, int y):
        return (self.lhSeq+1) * y + x

    cdef long doAlignment(self) except? 0:
        cdef int i  # vertical index
        cdef int j  # horizontal index
        cdef int idx
        cdef int jump
        cdef int delta
        cdef long score
        cdef long scoremax
        cdef long jmax
        cdef int    path

        
        if self.sequenceChanged:
            self.allocate()
            self.reset()
            
            for j in range(1,self.lhSeq+1):
                idx = self.index(j,0)
                self.matrix.matrix[idx].score = -2 * j  # <-- Gap score
                self.matrix.matrix[idx].path  = j
                                
            for i in range(1,self.lvSeq+1):
                idx = self.index(0,i)
                self.matrix.matrix[idx].score = 0
                self.matrix.matrix[idx].path  = -i
                
            for i in range(1,self.lvSeq+1):
                for j in range(1,self.lhSeq+1):
                    
                    # 1 - came from diagonal
                    idx = self.index(j-1,i-1)
                    # print "computing cell : %d,%d --> %d/%d" % (j,i,self.index(j,i),self.matrix.msize),
                    scoremax = self.matrix.matrix[idx].score + \
                               self.matchScore(j,i)
                    path = 0

                    # print "so=%f sd=%f sm=%f" % (self.matrix.matrix[idx].score,self.matchScore(j,i),scoremax),

                    # 2 - open horizontal gap
                    idx = self.index(j-1,i)
                    score = self.matrix.matrix[idx].score - 2 # <-- Gap score
                    if score > scoremax : 
                        scoremax = score
                        path = self.matrix.matrix[idx].path
                        if path >=0:
                            path+=1
                        else: 
                            path=+1
                    
                    # 3 - open vertical gap
                    idx = self.index(j,i-1)
                    score = self.matrix.matrix[idx].score - 2 # <-- Gap score
                    if score > scoremax : 
                        scoremax = score
                        path = self.matrix.matrix[idx].path
                        if path <=0:
                            path-=1
                        else:
                            path=-1
                                                    
                    idx = self.index(j,i)
                    self.matrix.matrix[idx].score = scoremax
                    self.matrix.matrix[idx].path  = path 
                                        
            scoremax=0
            jmax=self.lhSeq
            
            for j in range(self.lhSeq,1,-1):
                idx = self.index(j,self.lvSeq)
                if self.matrix.matrix[idx].score > scoremax:
                    scoremax=self.matrix.matrix[idx].score
                    jmax=j
#                    print j,scoremax,jmax
                    
            idx = self.index(self.lhSeq,self.lvSeq)
            self.matrix.matrix[idx].score=scoremax
            self.matrix.matrix[idx].path=self.lhSeq - jmax

        self.sequenceChanged=False

        idx = self.index(self.lhSeq,self.lvSeq)
        return self.matrix.matrix[idx].score
                   
    cdef void backtrack(self):
#        cdef list path=[]
        cdef int i
        cdef int j 
        cdef int p
        
        self.doAlignment()
        i=self.lvSeq
        j=self.lhSeq
        self.path=allocatePath(i,j,self.path)
        
        while (i or j):
            p=self.matrix.matrix[self.index(j,i)].path
            self.path.path[self.path.length]=p
            self.path.length+=1
#            path.append(p)
            if p==0:
                i-=1
                j-=1
            elif p < 0:
                i+=p
            else:
                j-=p
                
#        print path
        
    property seqA:
            def __get__(self):
                return self.horizontalSeq
            
            def __set__(self, seq):
                self.sequenceChanged=True
                self.horizontalSeq=seq
                self.hSeq=<char*>seq
                self.lhSeq=len(seq)
                
    property seqB:
            def __get__(self):
                return self.verticalSeq
            
            def __set__(self, seq):
                self.sequenceChanged=True
                self.verticalSeq=seq
                self.vSeq=<char*>seq
                self.lvSeq=len(seq)
                
    property score:
        def __get__(self):
            return self.doAlignment()
                    
    cdef void reset(self):
        self.sequenceChanged=True
        resetMatrix(self.matrix)
        
    
    cdef void clean(self):
        freeMatrix(self.matrix)
        freePath(self.path)
        
    def __dealloc__(self):
        self.clean()
        
    def __call__(self):
        cdef list hgaps=[]
        cdef list vgaps=[]
        cdef list b
        cdef int  hp=0
        cdef int  vp=0
        cdef int  lenh=0
        cdef int  lenv=0
        cdef int  h,v,p
        cdef int  i
        cdef object ali
        cdef long score
        
        if self.sequenceChanged:
            score = self.doAlignment()

        self.backtrack()
        for i in range(self.path.length-1,-1,-1):
            p=self.path.path[i]
            if p==0:
                hp+=1
                vp+=1
                lenh+=1
                lenv+=1
            elif p>0:
                hp+=p
                lenh+=p
                vgaps.append([vp,p])
                vp=0
            else:
                vp-=p
                lenv-=p
                hgaps.append([hp,-p])
                hp=0
            
        if hp:
            hgaps.append([hp,0])
        if vp:
            vgaps.append([vp,0])
                    
        return hgaps,vgaps
  
        
            
                