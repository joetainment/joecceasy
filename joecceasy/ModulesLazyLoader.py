'''
ModulesLazyLoaderMod
'''
import importlib

class ModulesLazyLoader(object):
    '''
    ModulesLazyLoader
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def __getattr__(self, attrStr):
        mod = importlib.import_module( attrStr )
        setattr( self, attrStr, mod)
        return mod
    
    def reloaded(self, attrStr ):
        mod = getattr(self, attrStr)
        mod = importlib.reload( mod )
        setattr( self, attrStr, mod )
        return mod