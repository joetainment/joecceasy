import os, sys, time
from . import Utils
from .Utils import classproperty


class VarWatcher:

    @classproperty
    def EasyMod(cls):
        import joecceasy
        return joeccEasy.Easy    ## *** fix this to be relative
    
    @classproperty
    def Easy(cls):
        return cls.EasyMod.Easy
    
    def __init__(self):
        self.easyMod = self.EasyMod
        self.easy = self..Easy
        self.updateInterval = 1
        self.varssDict={}
        self.lastUpdateTime = time.time()

    def add( self, var, action=None, actionArgs=(), actionKwargs={}, easyAction=None ):
        if action==None and easyAction==None:
            easyAction=print
        entry = Utils.Object()
        self.varsDict[var] = entry
        entry.var = var
        entry.actionArgs = actionArgs
        entry.actionKwargs = actionKwargs

        if easyAction==None:
            entry.action = action
        elif easyAction=='print':
            import subprocess, sys
            entry.action = (
                lambda var:
                  Easy.PrintVar( var )
            )
            entry.actionArgs=()
            entry.actionKwargs={}
        self.updateEntry( entry )
        return self
        

    def update( self ):
        for var, entry  in self.filesDict.items():
            newMtime = os.stat( filePath ).st_mtime
            if True:
                actionArgs = entry.actionArgs
                actionKwargs = entry.actionKwargs
                entry.action( *actionArgs, **actionKwargs )
            #else:
            #    raise Exception( f'action: {action} = Not implemented Yet! '
            #    
            #    if newMtime != entry.lastMtime:
            #        self.updateEntry( entry )
                
    def updateEntry( self, entry ):
        entry.lastMtime = os.stat( entry.filePath ).st_mtime
        action = entry.action
        actionArgs = entry.actionArgs
        actionKwargs = entry.actionKwargs
        if callable( action ):
            if entry.useFilePathAsFirstArg:
                action( entry.filePath, *actionArgs, **actionKwargs )
            else:
                action(  *actionArgs, **actionKwargs )
        return self
                
    def loop( self ):
        while True:
            #print( 'updating' )
            self.update()
            time.sleep( self.updateInterval )
        return self
        
