import pickle
import sys

from .indexer import Index

from .backtranslate.fasta import fasta
from . import samples
from orgasm.utils.dna import isDNA



def getIndex(config):
    '''
    
    @param config: a configuration object
    @return: an Indexer instance
    '''
    
    return Index(config['orgasm']['indexfilename'])

def getProbes(config):
    '''
    According to the configuration file and the --seeds option this function return the set
    of sequence probes to use
    
     
    @param config: a configuration object
    @return: a dictionary with gene name as key and the 
             nucleic or protein sequence as value
    @rtype: dict
    '''
    logger=config['orgasm']['logger']
    seeds =config['orgasm']['seeds']
    
    probes = {}
    
    if seeds is not None:
    
        for s in seeds:
            try:
                p = fasta(s)
                logger.info("Load probe sequences from file : %s" % s)
            except IOError:
                p = getattr(samples,s)
                logger.info("Load probe internal dataset : %s" % s)
                
            probes[s]=[p,{}]
                            
    return probes

def getAdapters(config):
    '''
    According to the configuration file and the --seeds option this function return the set
    of sequence probes to use
    
     
    @param config: a configuration object
    @return: a dictionary with gene name as key and the 
             nucleic or protein sequence as value
    @rtype: dict
    '''
    logger=config['orgasm']['logger']
    adapt5 =config['orgasm']['adapt5']
    adapt3 =config['orgasm']['adapt3']
    
    try:
        p3 = fasta(adapt3).values()
        logger.info("Load 3' adapter sequences from file : %s" % adapt3)
    except IOError:
        p3 = getattr(samples,adapt3)
        logger.info("Load 3' adapter internal dataset : %s" % adapt3)
                    
    try:
        p5 = fasta(adapt5).values()
        logger.info("Load 5' adapter sequences from file : %s" % adapt5)
    except IOError:
        p5 = getattr(samples,adapt5)
        logger.info("Load 5' adapter internal dataset : %s" % adapt5)
                    
    return (p3,p5)


def getSeeds(index,config,extension=".omx"):
    # looks if the internal blast was already run            
    output = config['orgasm']['outputfilename'] 
    logger=config['orgasm']['logger']
    kup=-1 if config['orgasm']['kup'] is None else config['orgasm']['kup']

    probes = getProbes(config)
    filename=output+extension
    
    if probes:
        # --seeds option on the command line -> look for these seeds
        logger.info("Running probes matching against reads...")
        
        for probename in probes:
            p = probes[probename][0]
            logger.info("    -> probe set: %s" % probename)
 
            seeds = index.lookForSeeds(p,
                                       mincov=config['orgasm']['seedmincov'],
                                       kup=kup,
                                       identity=config['orgasm']['identity'],
                                       logger=logger)
            
            probes[probename][1]=seeds
            
            logger.info("==> %d matches" % sum(len(seeds[i]) for i in seeds))
            
            
        with open(filename,"wb") as fseeds:
            pickle.dump(probes,fseeds)
    else:
        # no --seeds option on the command line -> load the previous results
                           
        try:
            with open(filename,'rb') as fseeds:
                probes = pickle.load(fseeds)
            logger.info("Load matches from previous run : %d probe sets restored" % len(probes))
            nm=0
            for k in probes:
                for m in probes[k][1].values():
                    nm+=len(m)
            logger.info("   ==> A total of : %d" % nm)
        except FileNotFoundError: 
            logger.info("No --seeds option specified and not previous matches stored")
            sys.exit(1)

    logger.info("Match list :") 

    covmax=0

    for probename in probes:
        p = probes[probename][0]
        s = probes[probename][1]
        nuc = all([isDNA(k) for k in p.values()])
        #print(s[list(s.keys())[0]])
        nbmatch = [(k,
                    sum(x[2] for x in s[k]),
                    sum(x[2] for x in s[k])*index.getReadSize() / len(p[k]) / (1 if nuc else 3)) for k in s]
                 
        nbmatch.sort(key=lambda x:-x[2])
        
        for gene, nb, cov in nbmatch:
            logger.info("     %-10s : %5d (%5.1fx)" % (gene,nb,cov))
        coverage=nbmatch[0][2]
        if coverage > covmax:
            covmax=coverage
        

    return covmax,probes

#def reloadAssembling