'''
Qtui

all callbacks can either be overridden in subclass or
provided in callback dict

*** todo :

    really needs way to run background jobs and keep
    running self.qapp.processEvents every short while
    until bg jobs  complete
    
    really, a more general joecceasy  wide system should exist for
    ultra easy tasks in other threads with thread safe dict
    for communication

    should change to have a mainWidget and mainLayout
    which are either central widget or it's children via
    things like tabViews and scrollLayout
    and initShould create it all using options
 
    toolbar
 
    Automatically create dock widgets on bottom for output and other tabs

    make easy way to build menus from dicts

'''

import os, sys
from PySide2.QtWidgets import QWidget, QFormLayout

## Get self mod and package __init__ mod (joecceasy modules)
## It is safe to get this without circular import problems
## because Qtui is only ever called 'lazily', after
## joecceasy module is fully loadedimport sys  ## just for SelfMod/SelfPak most imports later section
SelfPak=__import__(__package__)    
SelfMod=sys.modules[__name__]
import joecceasy
from . import EasyMod
from . import Easy
assert EasyMod.EasyModLoadingIsComplete==True

from .Utils import classproperty

try:
    import PySide2
except:
    QtGui = None
    print(  Mod_traceback.format_exc()  )
try:
    import PySide2.QtGui as QtGui
except:
    QtGui = None
    print(  Mod_traceback.format_exc()  )
try:
    import PySide2.QtWidgets as QtWidgets
except:
    QtWidgets = None
    print(  Mod_traceback.format_exc()  )  

try:
    import PySide2.QtCore as QtCore
except:
    QtCore = None
    print(  Mod_traceback.format_exc()  )  

Qtc = QtCore
Qtw = QtWidgets
Qtg = QtGui


class WidgetRecipe():
    def __init__(self, label, connections=None, name=None, kind='button',
            func=None,
            layout=None,
            useFuncNameInsteadOfLabelIfNoName=False,
            widget=None ):
        if connections is None:
            connections = {}
        self.connections = connections
        self.label = label
        self.kind = kind
        labelr = label.replace(" ", "" )
        if name is None:
            if func is not None:
                setattr( func, 'label', labelr )
                if useFuncNameInsteadOfLabelIfNoName:
                    name = func.__name__
                else: ## dont use
                    name = labelr
                    func.__name__ = name
            else: ##func doesn't exist
                name = labelr
        else: ## name exists
            if not func is None:
                func.__name__ = name

        self.name = name
        self.func = func
        self.layout = layout
        


class QtuiMeta( type ):
    @property
    def Qapp(cls):
        return cls.GetQapp()

class Qtui( PySide2.QtWidgets.QMainWindow, ):  #metaclass=QtuiMeta ):
    
    __QappSingleton = None
    @classproperty
    def WidgetRecipe(cls):
        return WidgetRecipe

    @classproperty
    def Qtc(cls):
        return QtCore
    @classproperty
    def QtCore(cls):
        return QtCore    
    @classproperty
    def Qtg(cls):
        return QtGui
    @classproperty
    def QtGui(cls):
        return QtGui
    @classproperty
    def Qtw(cls):
        return QtWidgets
    @classproperty
    def QtWidgets(cls):
        return QtWidgets

    @classproperty
    def Qapp(cls):
        return cls.GetQapp()
    
    @classproperty
    def SelfMod(cls):
        return SelfMod
        
    @classmethod
    def Exec(cls, *args, **kargs):
        qtui = cls( *args, **kargs )
        return qtui.exec_()
    
    @classmethod
    def ExecAndExit(cls,*args,**kargs ):
        """
        Exec Qapp and then sys.exit w qapp's returned
        """
        qtui = cls( *args, **kargs )
        qtui.execAndExit()
        return qtui ## this line may never be called
    
    @classmethod
    def GetQapp(cls, argv=None ):
        ## setup self.qapp and self.argv which are closely related
        if cls.__QappSingleton!=None:
            assert argv==None  ## we can't share qapp if giving custom args
            return cls.__QappSingleton
        else:
            existingQapp = QtWidgets.QApplication.instance()
            if existingQapp:
                assert argv==None  ## we can't share qapp if giving custom args
                cls.__QappSingleton = existingQapp
                return existingQapp
            else:
                if argv==None:
                    argv = sys.argv.copy()
                __QappSinglton = QtWidgets.QApplication( argv )
                return __QappSinglton
        
    def exec_(self): ## an extra name to match qt regular atApp.exec_() 
        return self.qapp.exec_()
        
    def execAndExit(self): ## an extra name to match qt regular atApp.exec_() 
        r =  self.qapp.exec_()
        Easy.Mods.sys.exit( r )
        return self  ## this line probably never reached

    def execQapp(self):
        return self.qapp.exec_() 

    def __init__(self, *args, **kargs ):
        argsOrig = args  ## like tuple(args) because args is already a tuple
        kargsOrig = kargs.copy()
        
        ## add specified entries from kargs
        ## or fallback defaults to self.
        dkargsForSelf = {
            ## kargs default fallbacks
            'qapp' : None,
            'argv' : None, ## the args to give qapp
            'papp' : None,
            'title' : 'Application',
            'appTitleToBeShownInMenu' : 'App',
            'tabTitle' : None, ## title of first default tab
            'windowTitle': None,  ## later we'll use self.title as fallback
            'instructionsText': None,  ## later we'll use self.title as fallback
            'iconPath': None,
            'appUserModelId' : 'mycompany.myproduct.subproduct.version', #taskbarIcon
            'callbacks' : {},  ## should be a dictionary like object
                ########  Callbacks should take 'self' at a minimum
                ########    They should generally take same args/kargs as
                ########    the wrapper functions
                ## createCentralWidget
                ## createCentralLayout
                ## update
                ## onGoClicked
                ## initAdditionalWidgetsIntoDefault
                ## initWidgetsPre
                ## initWidgetsPost                
        
            ## be careful of potential confusion with 
            ## setCentralWidget from centralWidget
            'updateInterval' : 30,
            'autoUpdateViaTimer' : True,
            'autoUpdatePapp' : None,
            ## todo noauto
            'autoShow' : True,
            'autoCreateLayout' : True,
            'autoCreateDefaultWidgetsInLayout' : True,
            'showInput' : True,
            'useTabs' : True,
            'useMenu' : True,
            'useOutput' : True,
            'autoExpandOutput':False,
            'useOutputToggleButton' : True,
            'useStatusBar' : True,
            'statusBarMsg' : '',
            'exitSleepTime' : 0.15,
            'minimumWidth': 400,
            'minimumHeight': 300,
            'widgetRecipes' : {},
            'widgets' : {}, ## Stores widgets
            'layouts' : {}, ## Stores layouts
        }
        Easy.DictOfDefaultsOntoObj( self, dkargsForSelf, kargs )
        
        dkargsLocal = {
            ## kargs default fallbacks
            'QMainWindowArgs' : tuple(), #tuple( (None, self.Qtc.Qt.WindowStaysOnTopHint,) ),
            'QMainWindowKargs' : {},
        }
        Easy.DictOfDefaultsOntoDict( dkargsLocal, kargs )
        
        ## add a couple fallback that are dependent on other fallbacks
        ## should add a nice Easy function to do selfToSelf fallbacks
        ## based on attribute names
        if self.windowTitle==None:
            self.windowTitle = self.title
        if self.tabTitle==None:
            self.tabTitle = self.title
    
        #if self.qapp==None:
        self.initQapp()
        
        ## after qapp,  set self.argv to something reasonable if it's None
        if self.argv==None:
            self.argv = sys.argv.copy()        


        super().__init__(
            *(  kargs[ 'QMainWindowArgs' ]  ),
            **(  kargs[ 'QMainWindowKargs' ]  ),
        )


        '''
        cb = self.callbacks.get( 'createCentralWidget' )
        if cb=!None:
            self.centralWidgetForLayout = cb()
        '''
        self.mainWidget = PySide2.QtWidgets.QWidget()
        self.mainLayout = PySide2.QtWidgets.QFormLayout()
        self.addToWidgets( 'mainLayout', self.mainLayout)
        self.mainWidget.setLayout( self.mainLayout )
        
                
        if self.useTabs==True:
            self.tabView = PySide2.QtWidgets.QTabWidget()
            self.tabBar = self.tabView.tabBar()
            ## widget for first tab page
            
            self.tabView.addTab( self.mainWidget, self.tabTitle )
            self.setCentralWidget( self.tabView )
        else:
            centralWidget = self.mainWidget #PySide2.QtWidgets.QWidget()
            self.setCentralWidget( centralWidget )
        #### self.centralWidget should now be valid via superclass ####

        self.initMenu()
        
        """
        cb = self.callbacks.get( 'createMainLayout' )
        if cb==None:
            self.centralLayout = PySide2.QtWidgets.QFormLayout()
        else:
            self.centralLayout = cb()
        """
        
        self.updateCallback = self.callbacks.get( 'update', None )

   
        import ctypes
        if os.name=='nt':    
            myappid = self.appUserModelId
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        if self.iconPath!=None:
            self.icon = QtGui.QIcon( self.iconPath )  
            self.setWindowIcon(  self.icon  )  
            self.qapp.setWindowIcon(  self.icon  )
            #print( self.icon )
        
        self.setWindowTitle( self.windowTitle )
        
        self.setMinimumWidth( self.minimumWidth )
        self.setMinimumHeight( self.minimumHeight )

        self.initOutput()
        
        ##self.initCentralWidget()
        ##self.initCentralLayout()
        self.initWidgetsPreWrapper()
        self.createWidgetsInCentralLayout()
        self.initWidgetsPostWrapper()        
        
        self.initUpdateTimer()
        
        statusBar = self.statusBar() ## first call also creates it
        ## 0 means no timeout
        statusBar.showMessage( self.statusBarMsg, 0 )
        if self.useStatusBar==True:
            statusBar.show()
        else:
            statusBar.hide()

        self.initWidgetRecipesWrapper()
        
        
        if self.autoShow==True:
            self.show()
        
    '''
    def initLayoutThenWidgets(self):

        self.initSetCentralWidget() ## create central widget
        
        self.initSetCentralLayout() ## create central widget
        self.initCreateDefaultWidgetsInLayout()
    '''            

    def initCentralWidget(self):        
        self.setCentralWidget( self.centralWidgetForLayout )
                               
    def initCentralLayout(self):
        self.centralWidgetForLayout.setLayout( self.centralLayout )
        
                
    def initLayout(self, *args, **kargs):
        """
        Override this to fill layout with your own widgets
        """

    def initOutput(self):
        self.outputDockWidget=QtWidgets.QDockWidget( "Output" )
        self.outputWidget=QtWidgets.QWidget(
            #parent=self.outputDockWidget
        )
        self.outputLayout=QtWidgets.QFormLayout()
        ## alyout has to be added first
        self.outputWidget.setLayout(self.outputLayout)
        self.outputDockWidget.setWidget( self.outputWidget )
        #if self.autoExpandOutput:
        #    self.outputDockWidget.show() ## show should be called on dock childs
        """                                 
        self.outputDockWidget.setFeatures(
              QtWidgets.QDockWidget.DockWidgetMovable
            | QtWidgets.QDockWidget.DockWidgetFloatable
            
            | QtWidgets.QDockWidget.DockWidgetClosable
        )
        """
        #QDockWidget.DockWidgetClosable
        #QDockWidget.DockWidgetMovable
        #QDockWidget.DockWidgetFloatable
        #QDockWidget.DockWidgetVerticalTitleBar
        #QDockWidget.NoDockWidgetFeatures        
        if self.useOutput:
            self.addDockWidget(
                QtCore.Qt.BottomDockWidgetArea,
                self.outputDockWidget,
            )
                
        self.outputTextEdit = PySide2.QtWidgets.QTextEdit( )
        self.outputTextEdit.setReadOnly( True )
        self.outputBlankLabel = QtWidgets.QLabel( "-" )
        self.outputLayout.addRow(self.outputTextEdit)
        
        self.outputToggleButton = QtWidgets.QPushButton("Output:  (Click Here To Hide)")
        ## left, top, right, bottom 
        self.outputLayout. setContentsMargins(5,0,5,10 )#addRow(self.outputBlankLabel)
        if self.useOutputToggleButton:
            self.outputDockWidget.setTitleBarWidget(
                self.outputToggleButton
            )
            self.outputDockWidget.titleBarWidget().clicked.connect(
                lambda: self.outputTextEditVisible('toggle'))
            if not self.autoExpandOutput:
                self.outputTextEditVisible(False)

    def initWidgetRecipes(self):
        pass
        
    def initWidgetRecipesWrapper(self):
        self.initWidgetRecipes()
        self.makeWidgetsFromRecipes()
        
        
    def initQapp(self):
        ## setup self.qapp and self.argv which are closely related        
        if self.qapp==None:
            self.qapp = self.GetQapp( self.argv )



    def initWidgetsPostWrapper(self):
        cb = self.callbacks.get( 'initWidgetsPost', None )
        if cb!=None: cb(self)
        self.initWidgetsPost()
        
    def initWidgetsPost(self):
        'pass'
        
    def initWidgetsPreWrapper(self):
        cb = self.callbacks.get( 'initWidgetsPre', None )
        if cb!=None: cb(self)
        self.initWidgetsPre()
        
    def initWidgetsPre(self):
        'pass'
        
    def initAdditionalWidgetsIntoDefaultWrapper(self):
        cb = self.callbacks.get( 'initAdditionalWidgetsIntoDefault', None )
        if cb!=None: cb(self)
        self.initAdditionalWidgetsIntoDefault()
        
        
    def initAdditionalWidgetsIntoDefault(self):
        'pass'
    
    def initMenu(self):
        if self.useMenu==True:
            self.menuEdit = self.menuBar().addMenu("&" + self.appTitleToBeShownInMenu )
            self.menuEditExitAction = self.menuEdit.addAction("E&xit" )
            self.menuEditExitAction.setShortcut(
                 PySide2.QtGui.QKeySequence("Ctrl+Q")
                #PySide2.QtGui.QKeySequence.Quit  doesn't work by default on windows,
                #and since other platforms all seem to use ctrl-q, we'll just use it' 
            )
            self.menuEditExitAction.triggered.connect(
                self.exitWrapper
            )
            
        
    def initUpdateTimer(self):
        if self.autoUpdateViaTimer==True:
            ## Create tmer based update loop
            self.updateTimer = QtCore.QTimer()
            self.updateTimer.timeout.connect( self.updateWrapper )
            self.setNextTimerUpdate()

    def addToWidgets( self, name, widget):
        self.widgets[name]=widget
        return widget

    def addToLayouts( self, name, layout):
        self.layouts[name]=layout
        return layout
    
    def appendToTextHeard(self, txt ):
        self.textHeard.append(txt)

        
    def createWidgetsInCentralLayout(self):
        """
        Override this to fill self.layout with your
        own widgets
        """
        if self.autoCreateDefaultWidgetsInLayout==True:
            self._createDefaultWidgetsInLayout()
        
    def _createDefaultWidgetsInLayout(self):
        if self.instructionsText!=None:
            self.instructionsLabel = \
                PySide2.QtWidgets.QLabel(self.instructionsText)
            self.instructionsLabel.setWordWrap(True)
            self.mainLayout.addRow(self.instructionsLabel)        
        
        self.inputLabel = PySide2.QtWidgets.QLabel("Input:")
        self.inputLabel.setWordWrap(True)
        self.inputTextEdit = PySide2.QtWidgets.QTextEdit( )        
        if self.showInput==True:
            self.mainLayout.addRow(self.inputLabel)
            self.mainLayout.addRow(self.inputTextEdit)
            ## Prep text edit area for testing
            self.inputTextEdit.selectAll()
            self.inputTextEdit.setFocus()            
        
        self.initAdditionalWidgetsIntoDefaultWrapper()
        
        """
        self.goButton = QtWidgets.QPushButton("Go")
        self.goButton.clicked.connect( self.onGoButtonClickedWrapper  )
        self.goButton.setFocus()
        self.mainLayout.addRow(self.goButton)
        """
                
        
        """
        self.outputLabel = PySide2.QtWidgets.QLabel("Output:")
        self.outputLabel.setWordWrap(True)
        self.outputLayout.addRow(self.outputLabel)
        """
        
        """
        self.exitButton = PySide2.QtWidgets.QPushButton("Exit")
        self.exitButton.clicked.connect( self.exitWrapper )
        self.mainLayout.addRow(self.exitButton)
        """
        
        #self.button.setFocus()

    
    '''    
    def onExitButtonClickedWrapper(self):
        cb = self.callbacks.get( 'onExitButtonClicked', None )
        if cb!=None:
            cb()
        self.onExitButtonClick()
        'pass'
        self.exit()
        
    def onExitButtonClick(self):
        'pass'
    '''
        
    def decorateFuncByAddingToWidgetRecipes( self, label,
            connections={},
            name=None,
            kind='button',
            layout=None,
            useFuncNameInsteadOfLabelIfNoName=False,
        ):
        #self = selfRef  ## not needed if this is a method with self
        def inner(func):
            nonlocal self
            nonlocal kind
            nonlocal name
            nonlocal connections
            nonlocal layout
            nonlocal useFuncNameInsteadOfLabelIfNoName
            import types
            recipe = WidgetRecipe( label, kind=kind, name=name,
                connections=connections, func=func, layout=layout,
                useFuncNameInsteadOfLabelIfNoName=useFuncNameInsteadOfLabelIfNoName,
            )
                    
            method = recipe.func
            setattr( self.__class__, recipe.name, method, ) #func,
            methodBack = getattr( self.__class__, recipe.name )
            recipe.func = methodBack
            
            
            self.widgetRecipes[recipe.name] = recipe
            #print( self.widgetRecipes )
            #print( self.widgetRecipes )        
            return func
        return inner
        
    def exit(self):
        """
        
        """
        'pass'
        
        
    def exitWrapper(self):
        cb = self.callbacks.get( 'onExit', None )
        if cb!=None:  cb()
        self.exit()
        
        try:
            ## *** todo  we could change app and win titles tosay exit
            self.statusBar().showMessage( "Exiting...", 0)
            self.exitButton.setText('Exiting...')
            self.exitButton.repaint()
        except:
            'pass'
        Easy.Sleep( self.exitSleepTime )            
        self.qapp.quit()
        ## the parent app will probably quit at this point if it has
        ## nothing else to do

                
    def outputTextEditVisible( self, newState=None ):
        if newState==True:
            self.outputToggleButton.setText("Output:  (Click Here To Hide)")            
            self.outputTextEdit.show()
        elif newState==False:
            self.outputToggleButton.setText("Show Output")
            self.outputTextEdit.hide()
        elif newState=='toggle':
            self.outputTextEditVisible(
                not self.outputTextEditVisible()
            )
        elif newState is None:
            return self.outputTextEdit.isVisible()
    

    def makeWidgetFromRecipe( self, recipe ):
        #print('making button')
        #print( f"recipe.name: {recipe.name}")
        layout = recipe.layout
        if layout is None:
            layout = self.mainLayout
        elif isinstance(layout,str):
            layout=self.layouts[layout]
        else:
            ""
            #print( "layout will be used directly" )
        if recipe.kind=='button':
            widget = Qtw.QPushButton( recipe.label )
        if recipe.kind=='label':
            widget = Qtw.QLabel( recipe.label )
        self.widgets[recipe.name]=widget
        if hasattr( recipe, 'connections' ):
            for signalName, slotRef in recipe.connections.items():
                sig = getattr( widget, signalName)
                if slotRef==True:
                    slot=( lambda:
                           getattr(self, recipe.name)()
                    )
                else:
                    if isinstance( slotRef, str):
                        slot=( lambda:
                           getattr(self, slotRef)()
                        )
                    else:
                        slot=slotRef
                sig.connect( slot )
        layout.addRow(
            widget
        )
    

    def makeWidgetsFromRecipes(self):
            for recipeName, recipe in self.widgetRecipes.items():
                self.makeWidgetFromRecipe( recipe )

    def onGoButtonClicked(self):
        #self.outputTextArea.insertPlainText("Go Button Clicked.\n")
        #self.outputTextArea.ensureCursorVisible()
        'pass'
        
    def onGoButtonClickedWrapper(self):
        cb = self.callbacks.get( 'onGoButtonClicked', None )
        if cb!=None:  cb(self)
        self.onGoButtonClicked()        

        
    def print(self, *args, doGui=True, doStandard=True, **kargs):
        ## *** todo  store curpos, move to end for insert,
        ## then restore the cursor's position if it wasn't at end
        sep = kargs.get('sep', ' ')
        end = kargs.get('end', '\n')
        if doGui:
            for a in args:
                self.outputTextEdit.insertPlainText( str(a) + str(sep) )
            if len(end)>0:
                self.outputTextEdit.insertPlainText( end )
            self.outputTextEdit.ensureCursorVisible()
        if doStandard:
            print( *args, **kargs )
        self.qapp.processEvents()
            
    def updateWrapper(self):
        self.update()
        if self.updateCallback!=None:
            self.updateCallback(self)
        self.setNextTimerUpdate()
        
    def update(self):
        'pass'

    def setNextTimerUpdate(self):
        self.updateTimer.start(
          self.updateInterval ## milliseconds
        )
    
    
    @property
    def statusbar(self):
        return self.statusBar()

oldDecoratorInnerCode = r"""

            #print( f"self is {self}" )
            #print("decorating")
            #print( f" func is {func} - {type(func)}" )
            #print( f"self is {self}" )
            #print("decorating")
            #print( f" func is {func} - {type(func)}" )
            #print( f"label is {label}" )
            #if not hasattr( self, 'buttonsFromDecorations' ):
            #setattr(self, 'buttonsFromDecorations', {} )
            #self.buttonsFromDecorations[label]=connections
            #print( f"func in decorateAsButton is: {func}" )
            #got = obj.__get__(self, self.__class__)
            #instance.bar
            #### could add to instance instead of class
            #import types
            #method = types.MethodType(  obj, self )
            #setattr( self, obj.__name__, method, )
            #print( getattr(self,funcLike.__name__))        
            #print( f"label is {label}" )
            #if not hasattr( self, 'buttonsFromDecorations' ):
            #setattr(self, 'buttonsFromDecorations', {} )
            #self.buttonsFromDecorations[label]=connections
            #print( f"func in decorateAsButton is: {func}" )
            #got = obj.__get__(self, self.__class__)
            #instance.bar
            #### could add to instance instead of class
            #import types
            #method = types.MethodType(  obj, self )
            #setattr( self, obj.__name__, method, )
            #print( getattr(self,funcLike.__name__))
            
            
            #types.MethodType( func, None, self.__class__ )  ## None doesn't work
            ## add it to the class so it can be access as a bound method
                
            #setattr( self.__class__, name, func, )
            #self.__class__[]            
            
"""


oldSlotRefStuff = r"""
    #slotName = recipe.func
                #print( slotName )
                #print( dir(self) )
                #slot = getattr( self, slotName )
                #slot()
            #elif callable(slotRef):
            #    slot=slotRef
            

"""


old02=r"""
        #getattr(self, n.fn)
        #n.s = getattr( n.w, 'clicked' ) #signal
        #n.w.clicked.connect(
        
        self.spacesToHyphensButton = Qtw.QPushButton('Convert Spaces To Hyphens')
        n.s.connect(
            self.onSpacesToHyphensButton )
        'Convert Spaces To Hyphens'
        fpr k,v in self.widgets.items():
            self.mainLayout.addRow(self.spacesToUnderscoresButton)
            self.mainLayout.addRow(self.spacesToHyphensButton)

"""

old03=r"""

            #for i,k in enumerate(  self.widgetRecipes  ):
            #    print( k, " ", i, )
"""
