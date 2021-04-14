import os, sys, traceback
from joecceasy import Easy ; Easy.Init()



#Easy.CdToScriptDir()

## When making a subclass, the init function
## should pass through
## *args, then optional arguments, then **kwargs
## using a pattern like below, otherwise there may be issues
## trying to pass through optional arguments
class JoeccToMp3Qtui(Easy.Qtui):
    def __init__(
            self,
            *args,
            title="JoeccToMp3",
            showInput=False,
            autoExpandOutput=True,
            useTabs=False,
            updateInterval=3000,
            useStatusBar=False,
            **kwargs
            ):
        
        self.isConversionInProgress=False
        
        ## default text for line edit
        self.ffmpegDefaultCommand = "ffmpeg"
        if os.name == 'nt':
            self.ffmpegDefaultCommand += ".exe"
            
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
         
    
        ffmpegLabel = self.widgets['ffmpegLabel'] = \
            self.Qtw.QLabel('FFMPEG executable, can be relative to script:')
        ffmpegLineEdit = self.widgets['ffmpegLineEdit'] = \
            self.Qtw.QLineEdit( self.ffmpegDefaultCommand )
        self.mainLayout.addRow( ffmpegLabel, ffmpegLineEdit)
        
        
        
        ## button
        button = self.widgets['button'] = \
            self.Qtw.QPushButton("Convert Files From Clipboard To Mp3")
        button.clicked.connect(self.onConvertButtonClicked)
        button.setFocus()
        self.mainLayout.addRow( button )
        
        self.menuEdit = self.menuBar().addMenu("&Edit")
        self.menuEditPasteAction = self.menuEdit.addAction("&Paste" )
        self.menuEditPasteAction.setShortcut( self.Qtg.QKeySequence.Paste )
        self.menuEditPasteAction.triggered.connect( self.convertFilesOnClipboard )

        button.setFocus()

    def onConvertButtonClicked(self):
        self.convertFilesOnClipboard()
        
    def convertFilesOnClipboard(self):
        if self.isConversionInProgress==True:
            return self
        self.isConversionInProgress=True
        btn = self.widgets['button']
        btnWasEnabled=btn.isEnabled()
        btn.setEnabled(False)
        oldLabel = btn.text()
        btn.setText("converting...")
        self.qapp.processEvents()
        
        clip = self.Qtg.QGuiApplication.clipboard()
        mimeData = clip.mimeData()
        urls = mimeData.urls()
        paths = [ path.toLocalFile()[0:] for path in urls ]
        #self.print( paths )
        
        import sys
        import subprocess
        import time
        import traceback
        args = paths
        argsCount = len(args)
        ffmpeg = self.widgets['ffmpegLineEdit'].text()
            ##"ffmpeg"  ## works on most linux systems if ffmpeg is installed
        self.print( "Attempting to convert to mp3 files...")
        try:
            for i, arg in enumerate(args):
                self.qapp.processEvents()
                inFile = arg
                outFile = self.replaceOrAppendExtension( inFile )
                ffmpeg = "ffmpeg"
                
                
                #infoCmd = '"ffmpeg"' + " -i " + inFile
                #subprocess.call( )
                spc = ' '
                isCopyCodec= self.widgets['codecCopyCheckbox'].isChecked()
                #False
                
                fOptsList  = []
                
                optBitrate  = self.widgets['bitrateLineEdit'].text()
                optBitrateStr = str(int( optBitrate ))
                optBitrateStr += 'k'
                
                fOptsFlagsList = [ '-vn', '-sn' ]
                
                fOptsCopyList = ['-c:a', 'copy']
                
                fOptsAudioBitrateList = \
                    ['-b:a',
                      optBitrateStr, 
                    ] 
                
                fOptsList.extend( fOptsFlagsList )
                
                if isCopyCodec:
                    fOptsList.extend( fOptsCopyList )
                else:
                    fOptsList.extend( fOptsAudioBitrateList )
                
                
                """
                cmd = ( '"' + ffmpeg + '"'
                    + " -n -i " 
                    + '"' + inFile + '"'
                    + fOptsStr
                    + '"' + outFile + '"'
                )
                """
                cmdList = [ ffmpeg, '-n',  '-i',
                          inFile ]
                cmdList.extend( fOptsList )
                cmdList.append(outFile) 
                cmd = cmdList
                
                #cmd = f"echo {inFile}"
                
                self.print( f"cmd is: {cmd}")
                ## -vn  discards video
                ## -sn discards subtitles
                ## -loglevel panic 
                msg = f"Converting file {i+1} of {argsCount}:\n" \
                        + "" + inFile + "\n" \
                        + "To:\n" \
                        + "" + outFile
                self.print( msg )
                
                try:
                    tub = Easy.Tubprocess( cmd )
                    for v in tub:
                        self.print( v.out, v.err, end='' )
                        
                    retVal = tub.wait() ## only needed for its cleanup sidefx         
                    if retVal == 0:
                        self.print( "\n...done" )
                    else:
                        self.print( f"...ffmpeg exited with error code: {retVal}" )
                except:
                    self.print( "An error occured."  )
                    self.print( Easy.Traceback()  )
                        
                
                    
                   
        except:    
            self.print( Easy.Traceback()  )
            
        self.print( Easy.TrimAndTab( r"""
            ##
            ...finished the attempt to process all files.
            Any failures/errors should be noted above.
            ===============================
        """) )
        
        btn.setText( oldLabel )
        btn.setEnabled( btnWasEnabled )
        self.isConversionInProgress=False
            
    def replaceOrAppendExtension( self, inFile ):
        ## default
        outFile = inFile + ".mp3"
        
        if False:
            "pass"
        elif inFile.endswith('.flac'):
            outFile = Easy.ReplaceEnd( inFile, ".flac", ".mp3" )
        elif inFile.endswith('.mp4'):
            outFile = Easy.ReplaceEnd( inFile, ".mp4", ".mp3" )
        elif inFile.endswith('.m4a'):
            outFile = Easy.ReplaceEnd( inFile, ".m4a", ".mp3" )
        elif inFile.endswith('.mkv'):
            outFile = Easy.ReplaceEnd( inFile, ".mkv", ".mp3" )
        elif inFile.endswith('.ogg'):
            outFile = Easy.ReplaceEnd( inFile, ".ogg", ".mp3" )
        elif inFile.endswith('.opus'):
            outFile = Easy.ReplaceEnd( inFile, ".opus", ".mp3" )
        elif inFile.endswith('.webm'):
            outFile = Easy.ReplaceEnd( inFile, ".webm", ".mp3" )
        elif inFile.endswith('.avi'):
            outFile = Easy.ReplaceEnd( inFile, ".avi", ".mp3" )
        elif inFile.endswith('.mpeg'):
            outFile = Easy.ReplaceEnd( inFile, ".mpeg", ".mp3" )
        elif inFile.endswith('.mpg'):
            outFile = Easy.ReplaceEnd( inFile, ".mpg", ".mp3" )
        elif inFile.endswith('.aac'):
            outFile = Easy.ReplaceEnd( inFile, ".aac", ".mp3" )
        elif inFile.endswith('.wav'):
            outFile = Easy.ReplaceEnd( inFile, ".wav", ".mp3" )
        else:
            "pass" ## Default case already handled


        return outFile


joeccToMp3Qtui = JoeccToMp3Qtui( )
exitCode = joeccToMp3Qtui.execQapp()
Easy.Exit( exitCode )