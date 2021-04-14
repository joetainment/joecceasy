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
        ##setattr(self, '0', self.JoecceasyModReloaded(attrStr) )
        
    def __getattr__(self, attrStr):
        if attrStr in self.__dict__:
            return self.__dict__[attrStr] 
            #getattr(self, attrStr)
        else:
            mod = importlib.import_module( attrStr )    
            setattr( self, attrStr, mod)
            return mod
    
    def __getitem__(self, index):
        if len(index)==0:
            raise AttributeError( f'ModuleLazyLoader has no attribute: {index}' )
        if hasattr( self, index):
            return getattr(self, index)
        ##
        ## if this point reached, we don't already have item at index 
        mod = importlib.import_module( index )               
        if not '.' in index:
            setattr( self, index, mod )
        ## now handle parent modules before dots in path
        pth = index
        ## successively add each parent in module 
        ## some, with dots in them, will only
        ## be reachable via indexing
        while '.' in pth:
            pthList = pth.split('.')
            pthList = pthList[ 0:-1 ]
            pth = '.'.join( pthList )
            stepMod = importlib.import_module( pth )
            #if not '.' in pth:
            setattr( self, pth, stepMod)
        return mod

    ## this is a long named attribute that shouldn't conflict with any module
    def joecceasyModReloaded(self, attrStr ):
        mod = getattr(self, attrStr)
        mod = importlib.reload( mod )
        setattr( self, attrStr, mod )
        return mod
    
    
""" workaround below can't actually work
because error itself comes from the module itself
lacking the child module, not the lazy loader.
:(

except AttributeError as err:
    msg += ( ""
        " If attempting to access a module inside another "
        + "module that doesn't automatically import the ones "
        + "inside of it, use the index access method to "
        + "get it, such as Easy.Mods['PySide2.QtWidgets'] "
        + "instead of Eay.Mods.PySide2.QtWidgets "
    )
    raise AttributeError( msg ).with_traceback(err.__traceback__)
"""    