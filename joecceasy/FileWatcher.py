import os, sys, time
from . import Utils

class FileWatcher:
    def __init__(self):
        self.updateInterval = 1
        self.filesDict={}

    def addFile( self, filePath, action=None, actionArgs=(), actionKwargs={}, useFilePathAsFirstArg=True, easyAction=None ):
        entry = Utils.Object()
        self.filesDict[filePath] = entry
        entry.filePath = filePath
        entry.lastMtime = os.stat( filePath ).st_mtime

        entry.actionArgs = actionArgs
        entry.actionKwargs = actionKwargs
        entry.useFilePathAsFirstArg=useFilePathAsFirstArg

        if easyAction==None:
            entry.action = action
        elif easyAction=='run':
            import subprocess, sys
            entry.action = (
                lambda filePath:
                  subprocess.run( [sys.executable, filePath ], capture_output=False )
            )
            entry.actionArgs=()
            entry.actionKwargs={}
        self.updateEntry( entry )
        return self
        

    def update( self ):
        for filePath, entry  in self.filesDict.items():
            newMtime = os.stat( filePath ).st_mtime
            actionArgs = entry.actionArgs
            actionKwargs = entry.actionKwargs
            if newMtime != entry.lastMtime:
                self.updateEntry( entry )
                
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
        
