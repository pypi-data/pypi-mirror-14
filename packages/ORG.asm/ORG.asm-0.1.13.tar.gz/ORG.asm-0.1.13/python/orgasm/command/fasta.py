'''
Created on 26 nov. 2014

@author: boyer
'''
from orgasm import getIndex, getSeeds
from orgasm.tango import restoreGraph, genesincontig

import os

__title__="Build a fasta file from the assembling graph"

default_config = { 
                 }

def addOptions(parser):
    parser.add_argument(dest='orgasm:indexfilename',  metavar='<index>', 
                        help='index root filename (produced by the orgasmi command)')
    
    parser.add_argument(dest='orgasm:outputfilename',     metavar='<output>', 
                                                          nargs='?', 
                                                          default=None,
                        help='output prefix' )
    

def fastaFormat(edge, title=None,  nchar=60):
    
    if title is None:
        title = 'Seq'
    
    lheader = []
        
    for k in ('weight', 'label', 'length', 'stemid', 'ingene'):
        lheader.append('%s=%s'%(k, edge[k]))
    
        
    l = ['; '.join(lheader)+";"]
    
    l[0] = '>%s_%d %s'%(title, edge['stemid'], l[0])

    
    seq  = edge['sequence']
    lseq = len(edge['sequence'])
    i=0
    while i < lseq:
        l.append(seq[i:i+60].decode('ascii'))
        i += 60
        
    return '\n'.join(l)

def run(config):

    logger=config['orgasm']['logger']
    output = config['orgasm']['outputfilename'] 

    r = getIndex(config)
    ecoverage,x = getSeeds(r,config)  
    
    asm = restoreGraph(output+'.oax',r,x)

    cg = asm.compactAssembling(verbose=False)
    
    genesincontig(cg,r,x)

    fastaout = open(output+".fasta","w")
        
    logger.info("Print the result as a fasta file")


    edges = [cg.getEdgeAttr(*i) for i in cg.edgeIterator(edgePredicate = lambda e : cg.getEdgeAttr(*e)['stemid']>0)]
    head, tail = os.path.split(output)
    
    for e in edges:
        print(fastaFormat(e, tail),file=fastaout)

