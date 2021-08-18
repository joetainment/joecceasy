import os, sys, traceback
from joecceasy import Easy


Easy.Init()

## Enums for radioButtons for where (atLoc)
ANYWHERE=0
START=1
END=2

#Easy.CdToScriptDir()

## When making a subclass, the init function
## should pass through
## *args, then optional arguments, then **kwargs
## using a pattern like below, otherwise there may be issues
## trying to pass through optional arguments
class JoeccClipboardEditor(Easy.Qtui):
    def __init__(
            self,
            *args,
            title="EasyClipboardEditor",
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
    

        ## Prfix and Suffix
        prefixLabel = self.widgets['prefixLabel'] = \
            self.Qtw.QLabel('Prefix:')
        prefixLineEdit = self.widgets['prefixLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty prefix by default
        self.mainLayout.addRow( prefixLabel, prefixLineEdit)

        prefixButton = self.widgets['prefixButton'] = \
            self.Qtw.QPushButton( 'Apply Prefix Now')
        self.mainLayout.addRow( None, prefixButton )
        prefixButton.clicked.connect( self.onPrefixButtonClicked )

        suffixLabel = self.widgets['suffixLabel'] = \
            self.Qtw.QLabel('Suffix:')
        suffixLineEdit = self.widgets['suffixLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty suffix by default
        self.mainLayout.addRow( suffixLabel, suffixLineEdit)

        suffixButton = self.widgets['suffixButton'] = \
            self.Qtw.QPushButton( 'Apply Suffix Now')
        self.mainLayout.addRow( None, suffixButton )
        suffixButton.clicked.connect( self.onSuffixButtonClicked )


        ## Seach and replace section
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

        searchButton = self.widgets['searchButton'] = \
            self.Qtw.QPushButton( 'Search And Replace Now')
        self.mainLayout.addRow( None, searchButton )
        searchButton.clicked.connect( self.onSearchButtonClicked )

        whereLabel = self.widgets['whereLabel'] = \
            self.Qtw.QLabel('Where:')
        whereButtonGroup = self.widgets['whereButtonGroup'] = \
            self.Qtw.QButtonGroup()
        atAnywhereRbutton = self.widgets['atAnywhereRbutton'] = \
            self.Qtw.QRadioButton("&Anywhere")
        atAnywhereRbutton.setChecked(True)
        self.mainLayout.addRow(whereLabel, atAnywhereRbutton)

        atStartRbutton = self.widgets['atStartRbutton'] = \
            self.Qtw.QRadioButton(" At &Start    ")
        atEndRbutton = self.widgets['atEndRbutton'] = \
            self.Qtw.QRadioButton("At &End    ", )
        self.mainLayout.addRow(atStartRbutton, atEndRbutton)
        # self.mainLayout.addRow(  )

        whereButtonGroup.addButton(atAnywhereRbutton, ANYWHERE)
        whereButtonGroup.addButton(atStartRbutton, START)
        whereButtonGroup.addButton(atEndRbutton, END)


        ## Case and Camel/Pascal/Spaces section
        uppercaseLabel = self.widgets['uppercaseLabel'] = \
            self.Qtw.QLabel('Uppercase:')
        uppercaseCheckbox = self.widgets['uppercaseLineEdit'] = \
            self.Qtw.QCheckBox( )  ## empty uppercase by default
        uppercaseCheckbox.setChecked(False)
        self.mainLayout.addRow(uppercaseLabel, uppercaseCheckbox)

        uppercaseButton = self.widgets['uppercaseButton'] = \
            self.Qtw.QPushButton( 'UPPERCASE Now')
        self.mainLayout.addRow( None, uppercaseButton )
        uppercaseButton.clicked.connect( self.onUpperButtonClicked )

        lowercaseLabel = self.widgets['lowercaseLabel'] = \
            self.Qtw.QLabel('Lowercase:')
        lowercaseCheckbox = self.widgets['lowercaseLineEdit'] = \
            self.Qtw.QCheckBox()  ## empty lowercase by default
        lowercaseCheckbox.setChecked(True)
        self.mainLayout.addRow(lowercaseLabel, lowercaseCheckbox)

        lowercaseButton = self.widgets['lowercaseButton'] = \
            self.Qtw.QPushButton('lowercase Now')
        self.mainLayout.addRow(None, lowercaseButton)
        lowercaseButton.clicked.connect(self.onLowerButtonClicked )

        
        pascalCaseLabel = self.widgets['pascalCaseLabel'] = \
            self.Qtw.QLabel('pascalCase:')
        pascalCaseCheckbox = self.widgets['pascalCaseLineEdit'] = \
            self.Qtw.QCheckBox( )  ## empty pascalCase by default
        pascalCaseCheckbox.setChecked(False)
        self.mainLayout.addRow(pascalCaseLabel, pascalCaseCheckbox)

        pascalCaseButton = self.widgets['pascalCaseButton'] = \
            self.Qtw.QPushButton( 'PascalCase Now')
        self.mainLayout.addRow( None, pascalCaseButton )
        pascalCaseButton.clicked.connect( self.onPascalButtonClicked )

        camelCaseLabel = self.widgets['camelCaseLabel'] = \
            self.Qtw.QLabel('camelCase:')
        camelCaseCheckbox = self.widgets['camelCaseLineEdit'] = \
            self.Qtw.QCheckBox()  ## empty camelCase by default
        camelCaseCheckbox.setChecked(True)
        self.mainLayout.addRow(camelCaseLabel, camelCaseCheckbox)

        camelCaseButton = self.widgets['camelCaseButton'] = \
            self.Qtw.QPushButton('camelCase Now')
        self.mainLayout.addRow(None, camelCaseButton)
        camelCaseButton.clicked.connect(self.onCamelButtonClicked )


        caseToSpaceLabel = self.widgets['caseToSpaceLabel'] = \
            self.Qtw.QLabel('caseToSpace:')
        caseToSpaceCheckbox = self.widgets['caseToSpaceLineEdit'] = \
            self.Qtw.QCheckBox()  ## empty caseToSpace by default
        caseToSpaceCheckbox.setChecked(True)
        self.mainLayout.addRow(caseToSpaceLabel, caseToSpaceCheckbox)

        caseToSpaceButton = self.widgets['CaseToSpaceButton'] = \
            self.Qtw.QPushButton('case to space Now')
        self.mainLayout.addRow(None, caseToSpaceButton)
        caseToSpaceButton.clicked.connect(self.onCaseToSpaceButtonClicked )



        ## Spaces Hypens Underscores
        ##     add a seperator option and have it affect other stuff too like camelCase
        ##     should also add an option to process lines
        ##     and perhaps to replace via escaped text?
        ##
        ## this can be a radio button?
        ## either than or explicit filds for  from  and  to
        # spacesToUndrscores
        # spacesToHyphens
        # hyphensToUndrscores
        # hyphensToSpaces
        # underscoresToHyphns
        # underscoresToSpaces


        """
        More xforms to add:
        
            CapStart
            LowStart
            
            CapAll
            LowAll
            
            Cap Each Word (opts: spaces, underscore, hyphens)
            Low each Word (opts: spaces, underscore, hyphens)
        
            camelCase from spaces
            PascalCase from spaces
            
            camelCase from underscores
            PascalCase from underscores
            
            camelCase from hyphens
            PascalCase from hyphens
            
            underscores to spaces
            spaces to underscores
            
            underscores to hyphens
            hyphens to underscore
            
            hyphens to spaces
            spaces to hyphens
            
        """

        """
        upperLabel = self.widgets['upperLabel'] = \
            self.Qtw.QLabel('Replace:')
        replaceLineEdit = self.widgets['replaceLineEdit'] = \
            self.Qtw.QLineEdit( '' ) ## empty replace by default
        self.mainLayout.addRow( replaceLabel, replaceLineEdit)


        searchButton = self.widgets['searchButton'] = \
            self.Qtw.QPushButton( 'Search And Replace Now')
        self.mainLayout.addRow( None, searchButton )
        searchButton.clicked.connect( self.onSearchButtonClicked )
        """

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
        
        
        """
        useExtensionLabel = self.widgets['useExtensionLabel'] = \
            self.Qtw.QLabel('Use Extension')
        useExtensionCheckbox = self.widgets['useExtensionCheckbox'] = \
            self.Qtw.QCheckBox()
        self.mainLayout.addRow( useExtensionLabel, useExtensionCheckbox )
        """ 




        
        ## button
        button = self.widgets['button'] = \
            self.Qtw.QPushButton("Modify Clipboard")
        button.clicked.connect(self.onModifyButtonClicked)
        button.setFocus()
        self.mainLayout.addRow( button )
        
        self.menuEdit = self.menuBar().addMenu("&Edit")
        self.menuEditPasteAction = self.menuEdit.addAction("&Paste" )
        self.menuEditPasteAction.setShortcut( self.Qtg.QKeySequence.Paste )
        self.menuEditPasteAction.triggered.connect( self.modifyClipboard )

        button.setFocus()

    def onPrefixButtonClicked(self):
        self.prefixClipboard()

    def prefixClipboard(self):
        prefix = self.widgets['prefixLineEdit'].text()
        text = self.clipboard.text()
        if not len(text):
            return
        text = prefix + text
        self.clipboard.setText( text )
        self.showResultInOutput( text )

    def onSuffixButtonClicked(self):
        self.suffixClipboard()

    def suffixClipboard(self):
        suffix = self.widgets['suffixLineEdit'].text()
        text = self.clipboard.text()
        if not len(text):
            return
        text = text + suffix
        self.clipboard.setText( text )
        self.showResultInOutput( text )

    def onSearchButtonClicked(self):
        self.searchClipboard()

    def searchClipboard(self):
        text = self.clipboard.text()
        if not len(text):
            return
        search  = self.widgets['searchLineEdit'].text()
        replace  = self.widgets['replaceLineEdit'].text()
        bSearch = len(search)
        atLoc = self.widgets['whereButtonGroup'].checkedId()

        if len(search):
            if atLoc==ANYWHERE:
                text = text.replace( search, replace)
            if atLoc==START:
                text = Easy.StrReplaceStart( text, search, replace)
            if atLoc==END:
                text = Easy.StrReplaceEnd( text, search, replace)

        self.clipboard.setText( text )
        self.showResultInOutput( text )



    def onUpperButtonClicked(self):
        self.upperClipboard()

    def upperClipboard(self):
        text = self.clipboard.text()
        if not len(text):
            return
        text = text.upper()
        self.clipboard.setText( text )
        self.showResultInOutput( text )

    def onLowerButtonClicked(self):
        self.lowerClipboard()

    def lowerClipboard(self):
        text = self.clipboard.text()
        if not len(text):
            return
        text = text.lower()
        self.clipboard.setText( text )
        self.showResultInOutput( text )








    def onCamelButtonClicked(self):
        self.camelClipboard()

    def camelClipboard(self):
        sep = ' '
        text = self.clipboard.text()
        if not len(text):
            return
        words = text.split( sep )
        words = [ word[0].upper()+word[1:]  for word in words    ]
        text = "".join(words)
        text = text[0].lower()+text[1:]
        self.clipboard.setText( text )
        self.showResultInOutput( text )

    def onPascalButtonClicked(self):
        self.pascalClipboard()

    def pascalClipboard(self):
        sep = ' '
        text = self.clipboard.text()
        if not len(text):
            return
        words = text.split( sep )
        words = [ word[0].upper()+word[1:]  for word in words    ]
        text = "".join(words)
        self.clipboard.setText( text )
        self.showResultInOutput( text )

    def onCaseToSpaceButtonClicked(self):
        self.caseToSpaceClipboard()

    def caseToSpaceClipboard(self):
        sep = ' '
        text = self.clipboard.text()
        if not len(text):
            return
        letters = []
        letters.append( text[0] )
        for i, letter in enumerate(text[1:]):
            #i=i+1
            if letter.isupper():
                letters.append( sep + letter)
            else:
                letters.append( letter )
        text = "".join(letters)
        self.clipboard.setText( text )
        self.showResultInOutput( text )







    def onModifyButtonClicked(self):
        self.modifyClipboard()

    def modifyClipboard(self):
        if self.isInProgress==True:
            return self
        self.isInProgress=True
        anyFailed=False
        dictOfRenamed = {}
        btn = self.widgets['button']
        btnWasEnabled=btn.isEnabled()
        btn.setEnabled(False)
        oldLabel = btn.text()
        btn.setText("modifying text in clipboard...")
        self.qapp.processEvents()

        text = self.clipboard.text( )  #'plain' )
        #text = ''.join( list(text) )
        textOrig=text

        prefix  = self.widgets['prefixLineEdit'].text()
        suffix  = self.widgets['suffixLineEdit'].text()
        search  = self.widgets['searchLineEdit'].text()
        replace  = self.widgets['replaceLineEdit'].text()

        bPrefix = len(prefix)
        bSuffix = len(suffix)
        bSearch = len(search)

        atLoc = self.widgets['whereButtonGroup'].checkedId()

        if len(search):
            if atLoc==ANYWHERE:
                text = text.replace( search, replace)
            if atLoc==START:
                text = Easy.StrReplaceStart( text, search, replace)
            if atLoc==END:
                text = Easy.StrReplaceEnd( text, search, replace)

        if bPrefix and bSuffix:
            text = prefix + text + suffix
        elif bPrefix:
            text = prefix + text
        elif bSuffix:
            text = text + suffix

        self.clipboard.setText( text )
        self.showResultInOutput( text )

        btn.setText( oldLabel )
        btn.setEnabled( btnWasEnabled )
        self.isInProgress=False

    def showResultInOutput(self, result ):
        self.print( "Clipboard text set to:" )
        self.print( result )


joeccClipboardEditor = JoeccClipboardEditor( )
exitCode = joeccClipboardEditor.execQapp()
Easy.Exit( exitCode )