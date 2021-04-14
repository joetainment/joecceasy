from joecceasy import Easy

Easy.Init()

## When making a subclass, the init function
## should pass through
## *args, then optional arguments, then **kwargs
## using a pattern like below, otherwise there may be issues
## trying to pass through optional arguments
class MyQtui(Easy.Qtui):
    def __init__(
            self,
            *args,
            title="Joecceasy Qtui  Example - Subclass",
            showInput=False,
            autoExpandOutput=True,
            updateInterval=3000,
            **kwargs
            ):
        super().__init__( *args,
            title=title,
            showInput=showInput,
            autoExpandOutput=autoExpandOutput,
            updateInterval=updateInterval,
            **kwargs,
        )
        

    def initAdditionalWidgetsIntoDefault( self ):
        qw = Easy.Mods.PySide2.QtWidgets
        msgBtn = self.widgets["msgButton"] = qw.QPushButton('click me')
        self.mainLayout.addRow(
            msgBtn   
        )
        msgBtn.clicked.connect( self.onMsgBtnCicked )
    
    def onMsgBtnCicked(self):
        self.print( "Msg button was clicked.")
        
    def update(self):
        self.print( 'Updating (triggered by timer)' )

myQtui = MyQtui( title="Joecceasy Qtui Example - Subclass" )
exitCode = myQtui.execQapp()
Easy.Exit( exitCode )