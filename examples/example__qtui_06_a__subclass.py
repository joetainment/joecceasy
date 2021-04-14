from joecceasy import Easy

Easy.Init()

## This shows a subclass with simple init args
## when we don't nee to pass through *args or **kargs
class MyQtui(Easy.Qtui):
    def __init__(
            self,
            title="Joecceasy Qtui  Example - Subclass",
            showInput=False,
            ):
        super().__init__(
            title=title,
            showInput=showInput,
            useOutput=False
        )
        

    def initAdditionalWidgetsIntoDefault( self ):
        qw = Easy.Mods.PySide2.QtWidgets
        self.mainLayout.addRow(
            qw.QLabel( 'This is an additional row!'),   
            qw.QPushButton('click me'),
        )

myQtui = MyQtui( title="Joecceasy Qtui Example - Subclass" )
exitCode = myQtui.execQapp()
Easy.Exit( exitCode )