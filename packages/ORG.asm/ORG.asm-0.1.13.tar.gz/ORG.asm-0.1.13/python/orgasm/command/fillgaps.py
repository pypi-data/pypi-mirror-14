'''
Created on 28 sept. 2014

@author: coissac
'''

import orgasm.samples

from orgasm import getIndex, getSeeds, getAdapters
from orgasm.tango import cutLowCoverage, cutSNPs,\
    estimateDeadBrancheLength, coverageEstimate, estimateFragmentLength,\
    genesincontig, scaffold, fillGaps, dumpGraph, restoreGraph

import sys


__title__="Fill gaps of a partially assembled graph"
 

default_config = { 'seeds' : None
                 }

def addOptions(parser):
    parser.add_argument(dest='orgasm:indexfilename',  metavar='index', 
                        help='index root filename (produced by the orgasmi command)')
    
    parser.add_argument(dest='orgasm:outputfilename',     metavar='output', 
                                                          nargs='?', 
                                                          default=None,
                        help='output prefix' )
    
    
    
    parser.add_argument('--minread',          dest='buildgraph:minread', 
                                              type=int, 
                                              action='store', 
                                              default=None, 
                        help='the minimum count of read to consider [default: <estimated>]')
    
    parser.add_argument('--coverage',         dest='buildgraph:coverage', 
                                              type=int, 
                                              action='store', 
                                              default=None, 
                        help='the expected sequencing coverage [default: <estimated>]')
    
    parser.add_argument('--minratio',         dest='buildgraph:minratio', 
                                              type=float, action='store', 
                                              default=None, 
                        help='minimum ratio between occurrences of an extension'
                             ' and the occurrences of the most frequent extension '
                             'to keep it. [default: <estimated>]')
    
    parser.add_argument('--mincov',           dest='buildgraph:mincov', 
                                              type=int, 
                                              action='store', 
                                              default=1, 
                        help='minimum occurrences of an extension to '
                             'keep it. [default: %(default)d]')
    
    parser.add_argument('--minoverlap',       dest='buildgraph:minoverlap', 
                                              type=int, 
                                              action='store', 
                                              default=None, 
                        help='minimum length of the overlap between '
                             'the sequence and reads to participate in '
                             'the extension. [default: <estimated>]')
    
    parser.add_argument('--smallbranches',    dest='buildgraph:smallbranches', 
                                              type=int, 
                                              action='store', 
                                              default=None, 
                        help='maximum length of the branches to cut during '
                             'the cleaning process [default: <estimated>]')
    
    parser.add_argument('--lowcomplexity',    dest='buildgraph:lowcomplexity', 
                                              action='store_true', 
                                              default=False, 
                        help='Use also low complexity probes')
    
    parser.add_argument('--back',             dest='orgasm:back', 
                                              type=int, 
                                              action='store', 
                                              default=None, 
                        help='the number of bases taken at the end of '
                             'contigs to jump with pared-ends [default: <estimated>]')
    
    parser.add_argument('--snp',              dest='buildgraph:snp', 
                                              action='store_true', 
                                              default=False, 
                        help='activates the SNP clearing mode')
    
    parser.add_argument('--adapt5',           dest ='orgasm:adapt5', 
                                              metavar='adapt5', 
                                              default='adapt5ILLUMINA', 
                                              type=str, 
                                              required=False,
                        help='adapter sequences used to filter reads beginning by such sequences'
                             '; either a fasta file containing '
                             'adapter sequences or internal set of adapter sequences '
                             'among %s' % (list(filter(lambda s: s.startswith('adapt5'),dir(orgasm.samples))),) +' [default: %(default)s]' )

    parser.add_argument('--adapt3',           dest ='orgasm:adapt3', 
                                              metavar='adapt3', 
                                              default='adapt3ILLUMINA', 
                                              type=str, 
                                              required=False,
                        help='adapter sequences used to filter reads ending by such sequences'
                             '; either a fasta file containing '
                             'adapter sequences or internal set of adapter sequences '
                             'among %s' % (list(filter(lambda s: s.startswith('adapt3'),dir(orgasm.samples))),) +' [default: %(default)s]' )

    parser.add_argument('--seeds',            dest ='fillgaps:seeds', 
                                              metavar='seeds', 
                                              default=None, 
                                              type=str, 
                        help='protein or nucleic seeds; either a fasta file containing '
                             'seed sequences or the name of one of the internal set of seeds '
                             'among %s' % str(list(filter(lambda s: s.startswith('prot') or 
                                                s.startswith('nuc'),dir(orgasm.samples))) ))


def estimateMinRead(index,minoverlap,coverage):
    MINREAD=10
    MINREADCOR=3
    MINOVERLAP=50
    minread =  (index.getReadSize() - minoverlap) * coverage / index.getReadSize()  / MINREADCOR
    if minread < MINREAD:
        minoverlap = index.getReadSize() - (MINREAD * MINREADCOR * index.getReadSize() / coverage)
        minread = MINREAD
    if  minoverlap< MINOVERLAP:
        minread =  MINREAD
        minoverlap = MINOVERLAP
    return minread,minoverlap


def run(config):
    
    logger=config['orgasm']['logger']
    output = config['orgasm']['outputfilename'] 
    lowfilter=not config['buildgraph']['lowcomplexity']
    coverageset=config['buildgraph']['coverage'] is not None
    snp=config['buildgraph']['snp']

    coverage = config['buildgraph']['coverage']
    smallbranches = config['buildgraph']['smallbranches']

    r = getIndex(config)
    xxx,x = getSeeds(r,config)  
    adapterSeq5,adapterSeq3 = getAdapters(config)
    
    asm = restoreGraph(output+'.oax',r,x)


    logger.info("Graph size %d" % len(asm))
    logger.info("Filling gaps")
       
    # Clean small unsuccessful extensions
    asm.cleanDeadBranches(maxlength=10)
    
    if len(asm) == 0:
        logger.error('The assembling is empty - Stop the assembling process')
        sys.exit(1)

    # reestimate coverage
    score,length,ecoverage = coverageEstimate(asm,x,r)  # @UnusedVariable
    print(score,length,ecoverage)
    if not coverageset:
        coverage = ecoverage  

    
    # and too low covered assembling
    if coverageset:
        cutLowCoverage(asm,int(coverage),terminal=True)
    else:
        cutLowCoverage(asm,int(coverage/4),terminal=True)
        
    
    # cleanup snp bubble in the graph    
    if snp:
        cutSNPs(asm)
    
    if config['buildgraph']['smallbranches'] is not None:
        smallbranches = config['buildgraph']['smallbranches']
    else:
        smallbranches = estimateDeadBrancheLength(asm)
        logger.info("     Dead branch length setup to : %d bp" % smallbranches)

    asm.cleanDeadBranches(maxlength=smallbranches)

    if len(asm) == 0:
        logger.error('The assembling is empty - Stop the assembling process')
        sys.exit(1)

    # reestimate coverage
    score,length,ecoverage = coverageEstimate(asm,x,r)  # @UnusedVariable
    print(score,length,ecoverage)
    
    if not coverageset:
        coverage = ecoverage  
    
    print(config['buildgraph']['minread'])
    if config['buildgraph']['minread'] is None:
        minread,minoverlap = estimateMinRead(r,config['buildgraph']['minoverlap'],coverage)
        print(minread)

        minread//=4
        if minread<5:
            minread=5
    else:
        minread,minoverlap = estimateMinRead(r,config['buildgraph']['minoverlap'],coverage)
        minread=config['buildgraph']['minread']
        
    print(coverage,length,minread)

    logger.info("coverage estimated : %d based on %d bp (minread: %d)" %(coverage,length,minread))
        
    meanlength,sdlength = estimateFragmentLength(asm)
    
    if config['orgasm']['back'] is not None:
        back = config['orgasm']['back']
    elif config['orgasm']['back'] is None and meanlength is not None:
        back = int(meanlength + 4 * sdlength)
        if back > 500:
            back=500
    else:
        back = 300
        
    if meanlength is not None:
        logger.info("Fragment length estimated : %f pb (sd: %f)" % (meanlength,sdlength))

    if snp:
        logger.info("Clean polymorphisms")
        cutSNPs(asm)
        
    cg = asm.compactAssembling(verbose=False)
    genesincontig(cg,r,x)
    scaffold(asm,cg,minlink=5,back=back,addConnectedLink=False)
    with open(output+'.intermediate.gml','w') as gmlfile:
        print(cg.gml(),file=gmlfile)
    
    ###################################################
    #
    # We now fill the gaps between the contigs
    #
    ###################################################
    
    delta = 1
       
    # Run the fill gap procedure    
    while  delta > 0 or delta < -2000 :
                   
        delta = fillGaps(asm,back=back,
                       minread=minread,
                       maxjump=0,
                       minoverlap=minoverlap,
                       cmincov=2,
                       emincov=int(coverage/4),
                       gmincov=int(coverage/4),
                       lowfilter=lowfilter,
                       adapters5 = adapterSeq5,
                       adapters3 = adapterSeq3,
                       snp=snp)

        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('==================================================================',file=sys.stderr)
        print('',file=sys.stderr)
        
        cg = asm.compactAssembling(verbose=False)
        genesincontig(cg,r,x)
        scaffold(asm,cg,minlink=5,back=back,addConnectedLink=False)
        with open(output+'.intermediate.gml','w') as gmlfile:
            print(cg.gml(),file=gmlfile)
        
        if meanlength is None:
            meanlength,sdlength = estimateFragmentLength(asm)
            if config['orgasm']['back'] is None and meanlength is not None:
                logger.info("Fragment length estimated : %f pb (sd: %f)" % (meanlength,sdlength))
                back = int(meanlength + 4 * sdlength)  
                if back > 500:
                    back=500
                         
        print('',file=sys.stderr)
        print('==================================================================',file=sys.stderr)
        print('',file=sys.stderr)
        
    ###################################################
    #
    # Finishing of the assembling
    #
    ###################################################

    if snp:
        logger.info("Clean polymorphisms")
        cutSNPs(asm)
        
    asi = len(asm)+1
    
    logger.info("Clean dead branches")
    while (asi>len(asm)):
        asi=len(asm)
        smallbranches = estimateDeadBrancheLength(asm)
        logger.info("     Dead branch length setup to : %d bp" % smallbranches)
        asm.cleanDeadBranches(maxlength=smallbranches)
        
    cg = asm.compactAssembling(verbose=False)
    
    if len(asm) == 0:
        logger.error('The assembling is empty - Stop the assembling process')
        sys.exit(1)

    score,length,ecoverage = coverageEstimate(asm,x,r)  # @UnusedVariable
    if not coverageset:
        coverage=ecoverage

    if snp:
        logger.info("Clean polymorphisms phase 2")
        cutSNPs(asm)
        
    logger.info("Clean low coverage terminal branches")
    if coverageset:
        cutLowCoverage(asm,int(coverage),terminal=False)
    else:
        cutLowCoverage(asm,int(coverage/2),terminal=True)
        logger.info("Clean low coverage internal branches")
        cutLowCoverage(asm,int(coverage/3),terminal=False)
        
        
    cg = asm.compactAssembling(verbose=False)     
        
    logger.info("Scaffold the assembly")
    scaffold(asm,cg,minlink=5,back=int(back),addConnectedLink=False)
    genesincontig(cg,r,x)

    with open(output+'.gml','w') as gmlfile:
        print(cg.gml(),file=gmlfile)

    dumpGraph(output+'.oax',asm)
