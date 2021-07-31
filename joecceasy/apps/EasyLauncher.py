import os
from joecceasy import Easy ; Easy.Init()


import win32com.client as Mod_win32com_client
import win32ui as Mod_win32ui
import win32gui as Mod_win32gui
from PySide2 import QtWidgets
from _signal import getsignal
from PySide2.QtWidgets import QLayoutItem


DEFAULT_PATH = r"C:\Users\joe\AppData\Roaming\Microsoft\Windows\Start Menu"

Qtw=Easy.Qtw
Qtc=Easy.Qtc
Qtg=Easy.Qtg
Qtui=Easy.Qtui
QtCore=Qtc
QtWidgets=Qtw
QtGui=Qtg


def getSignalsWithParents(source):
    #cls = source if isinstance(source, type) else type(source)
    #signal = type( QtCore.Signal() )
    obj=source ; i=0
    while i<99:
        getSignals(obj)
        obj=obj.parent()
        if obj is None: break
        i+=1
        
def keyPressEvent(self, event):
    print( "key was pressed" )
    

def getSignals(source):
    for entry in source.__class__.mro():
        for name in dir(entry):
            try:
                attr = getattr( entry, name )
                
                if 'signal' in str( type(attr) ).lower():
                ##if isinstance(attr, Qtc.SignalInstance ):
                    print( f"name: {name}    attr: {attr}    type: {type(attr) }" )
                
            except:
                Easy.PrintTraceback()
            #if isinstance(source, QtCore.Signal):
            #    print(name)
    

class Runner(object):
    def __init__( self ):
        self.shell = Mod_win32com_client.Dispatch("WScript.Shell")

    def makeWindowsFriendlyPath( path ):
        return path.replace( "\\", "/" )
    
    def run( self, path ):
        #print( "Launching " + path )
        ## Note: We don't need to 
        if  path[0] == '"'  :
            self.shell.run( path )
        else:
            try:
                self.shell.run( '"' + path + '"' )
            except Exception:
                Easy.PrintTraceback()
                self.print(
                    "Note that some shortcuts such as "
                    "VirtualBox shortcuts do not work "
                    "with this launcher due to WShell "
                    "limitations/complexities."
                )
                

                

class EasyLauncher(Easy.Qtui):
    def __init__(
            self,
            *args,
            **kwargs,
            ):
        
        kwargs = self.kwargsViaDict( kwargs, { 
            'title':"EasyLauncher",
            'showInput':False,
            'autoExpandOutput':False,
            'useTabs':False,
            'updateInterval':3000,
            'useStatusBar':False,
            'minimumWidth':900,
            'minimumHeight':450,
            'kwarg1-AddedViaKwargsViaDict':True,
            'kwarg2-AddedViaKwargsViaDict':False,
        })
        
        
        
        
        ## normally would
        ## will modify both kwargs and self via it's attribute dict if given one, otherwise won't modify kwargs but will apply ones in filter to object
        self.kwargsOntoSelf(  
            kwargs,
            
            {   ## keys/values to be added to kwargs
                'kwarg3-AddedViaAttrDict':True,
                'kwarg4-AddedViaAttrDict':False,
            },
            
            ## attributes from kwargs to apply to self
            filterInput={ ## only apply these keys from kwargs to self
                ## actual value is ignored is filterOutput is dict
                'kwarg1-AddedViaKwargsViaDict':1,
                'kwarg2-AddedViaKwargsViaDict':1,
            },                    
        )
        
        self.kwargsOntoSelf(
            None,  #not given kwargs as dest dict, just attr dict
            {
                'kwarg5-AddedViaAttrDict':True,
                'kwarg6-AddedViaAttrDict':False,
            }
        )

        self.dictOntoSelf( {
            'launcherColumns':7,
            'pathOfShortcuts':DEFAULT_PATH,               
        })
        
        superKwargs = self.dictCopyExclusive( kwargs,  "minimumHeight"  )
                     
        super().__init__( *args, **superKwargs
        )
        
        screen = self.screen()
        geo = screen.availableGeometry()
        self.move( 10,10 )
        self.resize( geo.width() - 10, geo.height() - 10 )
        
        ## look into ::text or ::label or something
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
            }
        """)
        
        #self.print( Easy.GetCwd() )
        
        
        
        self.gridWidget = Qtw.QWidget()
        self.gridWidget.setSizePolicy(Qtw.QSizePolicy.Expanding,Qtw.QSizePolicy.Expanding)
        self.gridLayout = Qtw.QGridLayout()
        self.gridWidget.setLayout( self.gridLayout ) 
        
        self.mainLayout.addRow( self.gridWidget )

        self.scrollArea = QtWidgets.QScrollArea( )
        self.scrollArea.setWidget( self.gridWidget )
        self.scrollArea.setWidgetResizable(True)
        #self.stayOpenLabel = Qtw.QLabel( "Stay open after launch:")
        self.stayOpenCheckbox = Qtw.QCheckBox( "Don't exit after launch:" )
        #self.stayOpenLabel = Qtw.QLabel( "Stay open after launch:")
        self.stayUnminimizedCheckbox = Qtw.QCheckBox( "Don't minimize after launch:" )
        #self.stayOpenCheckbox.setCheckeed( False )
        self.mainLayout.addRow( self.stayUnminimizedCheckbox, self.stayOpenCheckbox )
        self.mainLayout.addRow( self.scrollArea )



        self.runner = Runner()
        self.foundShortcuts = None
        self.getShortcuts()
        
        #self.print( "kwargs" )
        #self.print( kwargs )
        #self.print( self.foundShortcuts )
        
        self.buttons = Easy.OrderedDict()
        iterButtons = enumerate( self.foundShortcuts )
        gatheredBtns = self.gatheredBtns = []
        for i, shCut in iterButtons:
            shCutEnd = shCut
            shCutEnd = shCutEnd.split('/')[-1]
            shCutEnd = shCutEnd.split('\\')[-1]
            shCutEnd = os.path.splitext( shCutEnd )[0]

            btn = QtWidgets.QPushButton(    " "   +    shCutEnd[0:30]  )
            btn.setToolTip( shCutEnd )
            setattr( btn, "joeccAttr_fullPath", shCut )
            btn.clicked.connect( self.onLauncherButtonClicked )
            self.buttons[shCut]=btn
            gatheredBtns.append( btn )
            btn.setSizePolicy(Qtw.QSizePolicy.Expanding,Qtw.QSizePolicy.Fixed)
            
        gatheredBtns[0].setFocus()

        self.addButtonsAsColumns( gatheredBtns, columns = self.launcherColumns )
        #self.addButtonsAsRows( gatheredBtns, columns=3 )
        
        
        self.print( kwargs )
        
        self.print( "\n\n\n\n" )
        self.print( self.__dict__ )
        
    def addButtonsAsColumns(self, gatheredBtns, columns=3 ):
        by = columns
        lenTotal = len(gatheredBtns)
        excess =  lenTotal % by
        height = ( lenTotal // by )  + ( 1 if excess else 0 )
        
        iBtn = 0
        for c in range( by ):
            for r in range( height ):
                indexOfBtn = c*height + r
                if indexOfBtn < lenTotal:
                    btn = gatheredBtns[indexOfBtn]
                    self.gridLayout.addWidget( btn, r, c*height, )
        
    def addButtonsAsRows(self, gatheredBtns,  columns=3):
        by = columns
        i = 0
        while i<len(gatheredBtns):
            btnsForRow = tuple( gatheredBtns[ i: i+by ]   )
            #layoutItem = Qtw.QLayoutItem()
            for ii, btnForRow in enumerate(btnsForRow):
                self.gridLayout.addWidget( btnForRow, i//by, ii )                
            i+=by
        

        self.kbEventFilter = Qtui.KbEventFilterer(
            target=self.gridWidget,
            callback=self.onKbEventFilter,
            watched=['k'],
            #watchCase=True,
        )
        #self.gridWidget.installEventFilter(self.kbEventFilter)

    def onKbEventFilter(self, obj, event, info ):
        print(
            info.keys,
            #info.hasCtrl,
            #info.hasAlt, info.hasShift,
            #info.hasMeta, info.typ
        )
        return False

    def onLauncherButtonClicked(self):
        shCutPath = self.sender().joeccAttr_fullPath
        self.print( "Launching:\n" + shCutPath )
        self.runner.run( shCutPath )
        if not self.stayOpenCheckbox.isChecked():
            self.qapp.quit()
        elif not self.stayUnminimizedCheckbox.isChecked():
            self.showMinimized()


    def getShortcuts(self):
        ## Create an Runner object that will be used to run
        ## subprocesses
        
        ## Specify which paths will be used for launching programs
        searchPaths = []  #kargs.get('search_paths', [] )
        searchPaths.append(  self.pathOfShortcuts )
        #searchPaths.append(  r"C:\Users\joe\AppData\Roaming\Microsoft\Internet Explorer")
        
        
        foundFiles = []
        
        for s_path in searchPaths:
            for dir, subdirs, files in os.walk( s_path ):
                if os.path.abspath( s_path ) == os.path.abspath( dir ):
                    for file in files:
                     
                        found = os.path.join(dir, file)
                        foundFiles.append( found  )   
                        #print( "dir is:  "  +  str(root)  )
                        #print( "filename is:  "  +   str(filename)  )
        self.foundShortcuts = foundFiles
        #self.print( self.foundShortcuts )  

    def initAdditionalWidgetsIntoDefault( self ):
        "pass"

print( EasyLauncher.mro() )
    
easyLauncher = EasyLauncher( )
exitCode = easyLauncher.execQapp()
Easy.Exit( exitCode )


"""
        #w['layout'].setSizeConstraint( QtGui.QLayout.SetNoConstraint  )
        #w['layout'].setFieldGrowthPolicy( QtGui.QFormLayout.FieldsStayAtSizeHint )       
        #w['formScroll'] = QtGui.QScrollArea()
        #w['formScroll'].setLayout( w['layout'] )
"""
