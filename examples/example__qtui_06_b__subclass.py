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
            **kwargs
            ):
        super().__init__( *args,
            title=title,
            showInput=showInput,
            useOutput=False,
            useStatusBar=False,
            **kwargs,
        )

    def initAdditionalWidgetsIntoDefault( self ):
        qw = Easy.Mods.PySide2.QtWidgets
        self.mainLayout.addRow(   
            qw.QPushButton('click me'),
        )

myQtui = MyQtui( title="Joecceasy Qtui Example - Subclass" )
exitCode = myQtui.execQapp()
Easy.Exit( exitCode )