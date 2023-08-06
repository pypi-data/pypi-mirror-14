#!/usr/local/bin/python3.4
'''
orgasm -- shortdesc

orgasm is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2014 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import pkgutil
import argparse
import logging
import json

default_config = {

    'orgasm' :     { 'log'            : True,
                     'loglevel'       : 'INFO',
                     'outputfilename' : None,
                     'back'           : None,
                     'seeds'          : None,
                     'seedmincov'     : 1,
                     'kup'            : None,
                     'identity'       : 0.5,
                     'minlink'        : 5,
                     'version'        : False,
                     'progress'       : True
                   }
                 
}



from orgasm import command
from orgasm.version import version

__all__ = []
__version__ = version
__date__ = '2014-09-28'
__updated__ = '2014-09-28'

DEBUG = 1
TESTRUN = 0
PROFILE = 0



def loadCommand(name,loader):
    '''
    Load a command module from its name and an ImpLoader
    
    This function is for internal use
    
    @param name:   name of the module
    @type name: str 
    @param loader: the module loader
    @type loader: ImpLoader
    
    @return the loaded module
    @rtype: module 
    '''
    
    module = loader.find_module(name).load_module(name)
    return module

def getCommandsList():
    '''
    Returns the list of sub-commands available to the main orgasm command
    
    @return: a dict instance with key corresponding to each command and
             value corresponding to the module
             
    @rtype: dict
    '''
    cmds = dict((x[1],loadCommand(x[1],x[0])) 
                for x in pkgutil.iter_modules(command.__path__) 
                if not x[2])
    return cmds

def getLogger(config):
    '''
    Returns the logger as defined by the command line option
    or by the config file
    :param config:
    '''
 
    output = config['orgasm']['outputfilename'] 
    level  = config['orgasm']['loglevel'] 
    logfile= config['orgasm']['log'] 
    
    rootlogger   = logging.getLogger()
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

    stderrHandler = logging.StreamHandler(sys.stderr)
    stderrHandler.setFormatter(logFormatter)

    rootlogger.addHandler(stderrHandler)
    
    if logfile:
        fileHandler = logging.FileHandler("%s.log" % output)
        fileHandler.setFormatter(logFormatter)
        rootlogger.addHandler(fileHandler)
    
    try:
        loglevel = getattr(logging, level) 
    except:
        loglevel = logging.INFO
        
    rootlogger.setLevel(loglevel)
    
    config['orgasm']['logger']=rootlogger
    
    return rootlogger


class OaParser(argparse.ArgumentParser): 
   def error(self, message):
      sys.stderr.write('error: %s\n' % message)
      self.print_help()
      sys.exit(2)

def buildArgumentParser():
    parser = OaParser()
    
    parser.add_argument('--version',   dest='orgasm:version', 
                                       action='store_true', 
                                       default=False, 
                        help='Print the version of the Organelle Assembler')

    parser.add_argument('--no-log',    dest='orgasm:log', 
                                       action='store_false', 
                                       default=None, 
                        help='Do not create a logfile for the assembling')

    parser.add_argument('--no-progress', dest='orgasm:progress', 
                                       action='store_false', 
                                       default=None, 
                        help='Do not print the progress bar during assembling')

    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')
    
    commands = getCommandsList()
    
    for c in commands:
        module = commands[c]
        
        if hasattr(module, "run"):
            if hasattr(module, "__title__"):
                sub = subparsers.add_parser(c,help=module.__title__)
            else:
                sub = subparsers.add_parser(c)
    
            if hasattr(module, "addOptions"):
                module.addOptions(sub)
            
            sub.set_defaults(**{'orgasm:module' : module})
                        
    return parser

def buildDefaultConfiguration():
    global default_config
    
    commands = getCommandsList()
    
    for c in commands:
        module = commands[c]
    
        assert hasattr(module, "run")
        
        if hasattr(module, 'default_config'):
            default_config[c]=module.default_config
        else:
            default_config[c]={}
                        
    return default_config
        

def getConfiguration():
    global default_config

    if '__done__' in default_config:
        return default_config
    
    parser = buildArgumentParser()
    options = vars(parser.parse_args())
    
    config =  buildDefaultConfiguration()
    
    
    for k in options:
        section,key = k.split(':')
        s = config[section]
        if options[k] is not None:
            s[key]=options[k]
            
    if config['orgasm']['version']:
        print("The Organelle Assembler - Version %s" % __version__)
        sys.exit(0)

    if not 'module' in config['orgasm']:
        print('\nError: No oa command specified',file=sys.stderr)
        parser.print_help()
        sys.exit(2)
        
            
    if config['orgasm']['outputfilename'] is None:
        config['orgasm']['outputfilename']=config['orgasm']['indexfilename']
        
    getLogger(config)
    
    config['__done__']=True
            
    return config
    

if __name__ =="__main__":
    
    config = getConfiguration()    
                
    config['orgasm']['module'].run(config)
    
    
    