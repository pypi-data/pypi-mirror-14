# cython: language_level=3


from orgasm.indexer._orgasm cimport Index
from ._asmbgraph cimport AsmbGraph
from ._assembler cimport Assembler
from cpython.list cimport PyList_GET_SIZE
from functools import reduce
import sys

# cdef int isanchors(Index index ,int sid):
#     return index.getIds(index.getPairedRead(sid))[0]


cdef set setofreads(dict extensions):
    cdef set back=set()
    
    for x in extensions.values():
        back|=set(x[1])
        
    return back

cdef float isgrowing(list lastseeds):
    cdef int llast = PyList_GET_SIZE(lastseeds)
    cdef double i
    cdef int p = 0
    
    for i in lastseeds:
        if   i > 1.:
            p+=1
        elif i < 1.:
            p-=1
            
    return p / llast



cpdef AsmbGraph tango(Assembler self,
          list seeds,
          int minread=10,    float minratio=0.1, 
          int mincov=1,      int   minoverlap=40,
          bint lowfilter=True, 
          tuple adapters5=(), 
          tuple adapters3=(), 
          maxjump=0,restrict=None,
          int cycle=1, int nodeLimit=1000000,
          bint progress=True,
          logger=None):
    '''
    the :py:func:`~organsm.assembler.tango` function is the main assembling function. It extends selected
    seeds to produce the assembled sequence.
    
    :param seeds: a :py:class:`list` describing the extensions points. Each element of the list corresponds to 
                  a seed. A seed is described by a :py:class:`tuple` of two elements. 
                  
                  The first element is an integer value corresponding to the ``id`` of a read. if the ``id`` is greater than 0
                  the seed will be extended only if it is not already included in the assembling graph.
                  If the ``id`` is specified as a negative number, the seed will be included in the procedure
                  extension whatever if it is already member or not of the assembling graph.
                  
                  The second element of the :py:class:`tuple` is itself a :py:class:`tuple` contenaing or the 
                  :py:class:`None` value of a :py:class:`str` elements used to annotate the read.
                  
                  .. code-block :: python
                  
                      [(12347, ('matK',),0),(-37247,(None,),0)]
                  
                  In this example the structure describe two seeds. The first one corresponds to the
                  read 12347 annotated as belonging to the *matK* gene. The second corresponds to the
                  read 37247, without annotation. The process of extension will be run for the first seed
                  only if it is not already member of the assembling graph and always run on the second seed.
                  
    :type seeds: a :py:class:`list` of :py:class:`tuple`.
                     
    :param minread: Minimum count of reads having to be taken into account to extend an assembling path.
                    If this minimum count is not reach the extension of this path is stopped
    :type minread: :py:class:`int`
    
    :param minratio: A branch is added to the current path if the corresponding symbole **A**, **C**, **G** or **T**
                     represents at least a fraction of ``minratio``of the observed reads.
    :type minratio: :py:class:`float`
    
    :param mincov: To be considered, a read must be observed at least ``mincov`` in the total data set.
    :type mincov: :py:class:`int`
    
    :param minoverlap: Only reads overlaping the current extension point by ``minoverlap`` base pairs are
                       considered for the extension process. 
    :type minoverlap: :py:class:`int`
    
    :param lowfilter:
    :type lowfilter: :py:class:`bool`
    :param maxjump:
    :type maxjump: :py:class:`int`
    :param restrict:
    :type restrict: :py:class:`set` of :py:class:`int` values
    '''
        
    cdef int delta= 0
    cdef int sdelta= 0
    cdef str wheel= '|/-\\'
    cdef int lastprint=-1
    
    # a direct pointer to the read index
    cdef Index index = self._index
    
    # a direct pointer to the graph structure
    cdef AsmbGraph graph = self._graph
    
    # a direct access to the read length
    cdef int readLength = index.getReadSize()
    cdef int readmax    = index.len() + 1
    
    # extension cycle counter for the progress status monitoring
    cdef int icycle=0
    
    # count of missing reads in the graph (aka fake reads)
    cdef int fake=0
    
    # list of the stack size during the last 1000 cycles 
#    lastcycle=[]
    cdef list lastseeds=[0]
    cdef int addedseed=0
    
    # count of pair end jump on an extension branch
    # maxanchor = 0
    
    cdef str lastgene=None
    cdef float growing
    cdef int readid
    cdef int lgraph
    
    cdef dict rextensions
    cdef dict lextensions
    cdef dict backe
    cdef set back
    cdef list rk
    
    assert seeds is not None,'seeds cannot be set to None'
    
    while (PyList_GET_SIZE(seeds) > 0) and (graph.nodeCount() < nodeLimit) :
        
        #time.sleep(1)
        icycle+=1
        
        # Counter used to check how many seed will be added 
        # to the stack during the cycle
        addedseed=0

        # We pop one seed from the stack
        
        readid,(gene,),sdelta = seeds.pop()
        if sdelta < delta:
            delta = sdelta
            
        if gene is not None:
            lastgene = gene
        
#         # We test if the read poped out from the stack
#         # is just a jump mark
#         if readid==0:
#             maxanchor-=1
#             continue
        
        # Extension is forced if readid is provided as a negative number
        if readid < 0 or readid not in graph:
            
            if readid < 0:
                readid=-readid
            #print "\n==>",readid,str(gene)
            
            growing = isgrowing(lastseeds)
#             growing = (  float(sum([ls > 1. for ls in lastseeds])) \
#                        - float(sum([ls < 1. for ls in lastseeds]))) / len(lastseeds)
            
            if growing < -0.01 and delta > 0:
                delta-=1
                lastseeds=[1]*1000
            if growing > +0.01 and delta < 40:
                delta+=1
                lastseeds=[1]*1000
            
            if progress and (icycle % 50)==0 and sys.stderr.isatty(): 
                print("%s : %d bp [%4.1f%% fake reads; Stack size: %8d / %6.2f %d  Gene: %s " % (wheel[(icycle//10) % 4],
                                                                                                 len(graph)/2,
                                                                                                 float(fake)/(len(graph)+1)*200.,
                                                                                                 len(seeds),
                                                                                                 growing,
                                                                                                 delta,
                                                                                                 lastgene),
                       file=sys.stderr,
                       end="\r")
                      
            lgraph = graph.nodeCount()                                                                                           
            if logger is not None and lgraph!=lastprint and lgraph % 20000==0:
                lastprint=lgraph
                logger.info("%d bp [%4.1f%% fake reads; Stack size: %8d / %6.2f %d  Gene: %s " % (lgraph//2,
                                                                                                  float(fake)/(lgraph+1)*200.,
                                                                                                   PyList_GET_SIZE(seeds),
                                                                                                   growing,
                                                                                                   delta,
                                                                                                   lastgene))
                
    
            #
            # We add the read into the graph
            #
                
            #
            # extends the read on the right side
            #
            #logger.info("Before RCheck %s" % index.getRead(readid,1,readLength-1))
            rextensions = index.checkedExtensions(probe      = index.getRead(readid,1,readLength-1), 
                                                  adapters5  = adapters5,
                                                  adapters3  = adapters3,
                                                  minread    = minread+delta, 
                                                  minratio   = minratio, 
                                                  mincov     = mincov,  
                                                  minoverlap = minoverlap+delta, 
                                                  extlength  = 1,
                                                  lowfilter  = lowfilter,
                                                  restrict   = restrict,
                                                  exact      = True)
            #print >>sys.stderr,"After RCheck"
            #print(rextensions)
            #
            # Build a bijective relationship for the right extensions
            #
            rk=list(rextensions.keys())
            for k in rk:
                #print >>sys.stderr,"Before RICheck",index.getRead(-rextensions[k][1][0],1,readLength-1)
                backe = index.checkedExtensions(probe      = index.getRead(-rextensions[k][1][0],1,readLength-1), 
                                                adapters5  = adapters5,
                                                adapters3  = adapters3,
                                                minread    = minread+delta, 
                                                minratio   = minratio, 
                                                mincov     = mincov,  
                                                minoverlap = minoverlap+delta, 
                                                extlength  = 1,
                                                lowfilter  = lowfilter,
                                                restrict   = restrict,
                                                exact      = True)
                #print >>sys.stderr,"After RICheck"

                # back = set(reduce(lambda p,q:p+q,[backe[y][1] for y in backe],[]))
                back = setofreads(backe)
                
                if -readid not in back:
                    #print "Remove R extension : ",k
                    del rextensions[k]
            
    
            #print >>sys.stderr,"Before LCheck",index.getRead(-readid,1,readLength-1)
            lextensions = index.checkedExtensions(probe      = index.getRead(-readid,1,readLength-1), 
                                                  adapters5   = adapters5,
                                                  adapters3   = adapters3,
                                                  minread    = minread+delta, 
                                                  minratio   = minratio, 
                                                  mincov     = mincov,  
                                                  minoverlap = minoverlap+delta, 
                                                  extlength  = 1,
                                                  lowfilter  = lowfilter,
                                                  restrict   = restrict,
                                                  exact      = True)
            #print >>sys.stderr,"After LCheck"
     
            #
            # Build a bijective relationship for the left extensions
            #
            lk=list(lextensions.keys())
            for k in lk:
                #print >>sys.stderr,"Before LICheck",index.getRead(-lextensions[k][1][0],1,readLength-1)
                backe = index.checkedExtensions(probe      = index.getRead(-lextensions[k][1][0],1,readLength-1), 
                                                adapters5   = adapters5,
                                                adapters3   = adapters3,
                                                minread    = minread+delta, 
                                                minratio   = minratio, 
                                                mincov     = mincov,  
                                                minoverlap = minoverlap+delta, 
                                                extlength  = 1,
                                                lowfilter  = lowfilter,
                                                restrict   = restrict,
                                                exact      = True)
                #print >>sys.stderr,"After LICheck"
                
                # back = set(reduce(lambda p,q:p+q,[backe[y][1] for y in backe],[]))
                back = setofreads(backe)
                
                if readid not in back:
                    #print "Remove L extension : ",k
                    del lextensions[k]
                    
    #        print "Rext = ",rextensions
    #        print "Lext = ",lextensions
    
            if rextensions or lextensions:
                node  = graph.addNode(readid)
                node['gene']=gene
                if 'cycle' not in node:
                    node['cycle']=cycle
                if readid < readmax:
                    node['fake5']=0
                    node['fake3']=0
                else:
                    fake+=1
#                     node['graphics']={'fill':"#00FF00"}
    
    #        print "R",len(seq)
    
            for ex in rextensions:
                data = rextensions[ex]
                coverage = data[0]
    #            print ex,data
                
                nodeindexE,c,s = index.getIds(data[1][0])  # @UnusedVariable
                                    
                if nodeindexE in graph:
                    if data[1][0] not in s:
                        nodeindexE=-nodeindexE
                    # if readid!=-nodeindexE:
                    edges = graph.addEdge(readid,nodeindexE)
                    edges[1]['coverage']=coverage
                    edges[2]['coverage']=coverage
#                     edges[1]['label']="%s (%d)" % (edges[1]['ext'],coverage)
#                     edges[2]['label']="%s (%d)" % (edges[2]['ext'],coverage)
                    # else:
                    #     print >>sys.stderr,"\nWARNING : self loop on %d" % nodeindexE
        #              print "linked"
                else:
        #              print "not linked"
                    seeds.append((nodeindexE,(None,),int(delta)))
                    addedseed+=1
                                
            #
            # extends the read on the left side
            # which is equivalent to extend on the right side
            # the reverse complement of the read
            #            
     
            for ex in lextensions:
                data = lextensions[ex]
                coverage = data[0]
    #            print ex,data
    
                nodeindexE,c,s = index.getIds(data[1][0])                               # @UnusedVariable
                                        
                if nodeindexE in graph:
                    if data[1][0] not in s:
                        nodeindexE=-nodeindexE
                    edges = graph.addEdge(-readid,nodeindexE)
                    edges[1]['coverage']=coverage
                    edges[2]['coverage']=coverage
#                     edges[1]['label']="%s (%d)" % (edges[1]['ext'],coverage)
#                     edges[2]['label']="%s (%d)" % (edges[2]['ext'],coverage)
                else:
                    seeds.append((nodeindexE,(None,),int(delta)))
                    addedseed+=1
            
            lastseeds.append((len(lextensions)+len(rextensions))/2.)
            if PyList_GET_SIZE(lastseeds) > 1000:
                lastseeds=lastseeds[-1000:]         

                
                        
    return graph
