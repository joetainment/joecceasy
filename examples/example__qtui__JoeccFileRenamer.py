import os, sys, traceback
from joecceasy import Easy ; Easy.Init()

ANYWHERE=0
START=1
END=2

#Easy.CdToScriptDir()

## When making a subclass, the init function
## should pass through
## *args, then optional arguments, then **kwargs
## using a pattern like below, otherwise there may be issues
## trying to pass through optional arguments
class JoeccFileRenamer(Easy.Qtui):
    def __init__(
            self,
            *args,
            title="JoeccFileRenamer",
            showInput=False,
            autoExpandOutput=True,
            useTabs=False,
            updateInterval=3000,
            useStatusBar=False,
            **kwargs
            ):
        
        self.isInProgress=False
        
        self.bitrateDefault="320"
            
        super().__init__( *args,
            title=title,
            showInput=showInput,
            autoExpandOutput=autoExpandOutput,
            updateInterval=updateInterval,
            useTabs=useTabs,
            useStatusBar=useStatusBar,
            **kwargs,
        )
        
        #self.print( Easy.GetCwd() )

    def initAdditionalWidgetsIntoDefault( self ):
        """
        bitrateLabel = self.widgets['bitrateLabel'] = \
            self.Qtw.QLabel('Bitrate (as kbps):')
        bitrateLineEdit = self.widgets['bitrateLineEdit'] = \
            self.Qtw.QLineEdit( self.bitrateDefault )
        self.mainLayout.addRow( bitrateLabel, bitrateLineEdit)
        
        codecCopyLabel = self.widgets['codecCopyLabel'] = \
            self.Qtw.QLabel('Copy audio stream via "-c:a copy":')
        codecCopyCheckbox = self.widgets['codecCopyCheckbox'] = \
            self.Qtw.QCheckBox()
        self.mainLayout.addRow( codecCopyLabel, codecCopyCheckbox )
        """
    
        """ should have:
        name prefix  replace/replace  suffix
     
        ext  prefix, suffix, replace/replace
        
        name and ext  replace replace
        
        
        could have more...
            replaceOnlyAtStart or at end
             incrementerOrReplace        
        lstrip by int starting at index
        rstrip by int starting at index
        
        could read metadata
        
        
        """
    
    
        prefixLabel = self.widgets['prefixLabel'] = \
            self.Qtw.QLabel('Prefix:')
        prefixLineEdit = self.widgets['prefixLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty prefix by default
        self.mainLayout.addRow( prefixLabel, prefixLineEdit)
            
        suffixLabel = self.widgets['suffixLabel'] = \
            self.Qtw.QLabel('Suffix:')
        suffixLineEdit = self.widgets['suffixLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty suffix by default
        self.mainLayout.addRow( suffixLabel, suffixLineEdit)
            
        searchLabel = self.widgets['searchLabel'] = \
            self.Qtw.QLabel('Search:')
        searchLineEdit = self.widgets['searchLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty search by default
        self.mainLayout.addRow( searchLabel, searchLineEdit)
        
        replaceLabel = self.widgets['replaceLabel'] = \
            self.Qtw.QLabel('Replace:')
        replaceLineEdit = self.widgets['replaceLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty replace by default
        self.mainLayout.addRow( replaceLabel, replaceLineEdit)
        
        #at start and1 at end
        """    
        searchAtStartLabel = self.widgets['searchLabel'] = \
            self.Qtw.QLabel('Search:')
        searchLineEdit = self.widgets['searchLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty search by default
        self.mainLayout.addRow( searchLabel, searchLineEdit)
        
        replaceLabel = self.widgets['replaceLabel'] = \
            self.Qtw.QLabel('Replace:')
        replaceLineEdit = self.widgets['replaceLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty replace by default
        self.mainLayout.addRow( replaceLabel, replaceLineEdit)
        """
        
        
        useExtensionLabel = self.widgets['useExtensionLabel'] = \
            self.Qtw.QLabel('Use Extension')
        useExtensionCheckbox = self.widgets['useExtensionCheckbox'] = \
            self.Qtw.QCheckBox()
        self.mainLayout.addRow( useExtensionLabel, useExtensionCheckbox )
         
         
        whereLabel = self.widgets['whereLabel'] = \
            self.Qtw.QLabel('Where:')
        whereButtonGroup = self.widgets['whereButtonGroup'] = \
            self.Qtw.QButtonGroup()
        atAnywhereRbutton = self.widgets['atAnywhereRbutton'] = \
            self.Qtw.QRadioButton( "&Anywhere" )
        atAnywhereRbutton.setChecked(True)
        self.mainLayout.addRow( whereLabel, atAnywhereRbutton )

        
        atStartRbutton = self.widgets['atStartRbutton'] = \
            self.Qtw.QRadioButton(" At &Start    " )
        atEndRbutton = self.widgets['atEndRbutton'] = \
            self.Qtw.QRadioButton("At &End    ", )
        self.mainLayout.addRow( atStartRbutton, atEndRbutton )
        #self.mainLayout.addRow(  )
            
        whereButtonGroup.addButton(atAnywhereRbutton, ANYWHERE)
        whereButtonGroup.addButton(atStartRbutton, START)
        whereButtonGroup.addButton(atEndRbutton, END )
         
        
        
        ## button
        button = self.widgets['button'] = \
            self.Qtw.QPushButton("Rename Files On Clipboard")
        button.clicked.connect(self.onRenameButtonClicked)
        button.setFocus()
        self.mainLayout.addRow( button )
        
        self.menuEdit = self.menuBar().addMenu("&Edit")
        self.menuEditPasteAction = self.menuEdit.addAction("&Paste" )
        self.menuEditPasteAction.setShortcut( self.Qtg.QKeySequence.Paste )
        self.menuEditPasteAction.triggered.connect( self.renameFilesOnClipboard )

        button.setFocus()

    def onRenameButtonClicked(self):
        self.renameFilesOnClipboard()
        
    def renameFilesOnClipboard(self):
        if self.isInProgress==True:
            return self
        self.isInProgress=True
        anyFailed=False
        dictOfRenamed = {}
        btn = self.widgets['button']
        btnWasEnabled=btn.isEnabled()
        btn.setEnabled(False)
        oldLabel = btn.text()
        btn.setText("renaming files on clipboard...")
        self.qapp.processEvents()
        
        clip = self.Qtg.QGuiApplication.clipboard()
        mimeData = clip.mimeData()
        urls = mimeData.urls()
        self.print(urls)
        
        prefix  = self.widgets['prefixLineEdit'].text()
        suffix  = self.widgets['suffixLineEdit'].text()
        search  = self.widgets['searchLineEdit'].text()
        replace  = self.widgets['replaceLineEdit'].text()
        paths = [ path.toLocalFile()[0:] for path in urls ]
        #self.print( paths )
        atLoc = self.widgets['whereButtonGroup'].checkedId()
        bUseExt = self.widgets['useExtensionCheckbox'].isChecked()
        bSearch = len( search ) > 0
        print( f'bSearch {bSearch}  bUseExt {bUseExt} ')
        
        import sys
        import subprocess
        import time
        import traceback
        pathsCount = len(paths)
        #ffmpeg = self.widgets['ffmpegLineEdit'].text()
            ##"ffmpeg"  ## works on most linux systems if ffmpeg is installed
        self.print( "Attempting to rename files...")
        try:
            for i, path in enumerate(paths):
                    
                self.qapp.processEvents()
                
                import os
                
                if os.path.sep=='\\':
                    path=path.replace( '/', '\\' )
                    
                pathOld = path
                dir, fbnameOld, extOld =Easy.SplitDirFileExt( pathOld )
                if bUseExt:
                    fbnameOld, extOld = fbnameOld + extOld, ''

                if bSearch:
                    if atLoc==ANYWHERE:
                        fbnameRe = fbnameOld.replace( search, replace)
                    if atLoc==START:
                        fbnameRe = Easy.StrReplaceStart( fbnameOld, search, replace)
                    if atLoc==END:
                        fbnameRe = Easy.StrReplaceEnd( fbnameOld, search, replace)
                else:    
                    fbnameRe = fbnameOld

                fbnameNew = prefix + fbnameRe + suffix #oldname #+ suffix
                
                pathNew = Easy.JoinDirFileExt( dir, fbnameNew, extOld )
                self.print( f"pathOld:  {pathOld}")
                self.print( f"pathNew:  {pathNew}")             
                try:
                    os.rename( pathOld, pathNew )
                    dictOfRenamed[pathNew] = True
                except:
                    anyFailed=True
                    self.print( Easy.Traceback()  )
                    self.print( "An error occured."  )
                    
        except: 
            anyFailed=True   
            self.print( Easy.Traceback()  )
            
        if not anyFailed:
            'copy new urls!'
            toClip=[]
            for c in dictOfRenamed:
                if os.path.sep=='\\':
                    c = c.replace( '\\/', '/' )
                toClip.append( 'file:///' + c )
            newMimeData = self.Qtc.QMimeData()
            newMimeData.setUrls( toClip )
            clip.setMimeData( newMimeData )
            
        self.print( Easy.TrimAndTab( r"""
            ##
            ...finished the attempt to rename all files.
            Any failures/errors should be noted above.
            ===============================
        """) )
        
        btn.setText( oldLabel )
        btn.setEnabled( btnWasEnabled )
        self.isInProgress=False


joeccFileRenamer = JoeccFileRenamer( )
exitCode = joeccFileRenamer.execQapp()
Easy.Exit( exitCode )