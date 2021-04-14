from joecceasy import Easy
QtWidgets = Easy.Mods['PySide2.QtWidgets']

instructions = "Instructions: " \
"This is some instructional text. It can be multiple lines if you like. " \
"Click Go to get a message!\n"


def additionalWidgets( ui ):
    qw = Easy.Mods.PySide2.QtWidgets
    ui.mainLayout.addRow(
        qw.QLabel( 'This is an additional row!'),   
        qw.QPushButton('click me'),
    )
    

qtui = Easy.Qtui( title="JoecceasyQtuiExample",
    instructionsText = instructions,
    showInput=False,
    callbacks = {
        'initAdditionalWidgetsIntoDefault': additionalWidgets,
        'initWidgetsPre': additionalWidgets,
        'initWidgetsPost': additionalWidgets
    },
)
exitCode = qtui.execQapp() ## qtui.qapp.exec_() would do the same
Easy.Exit( exitCode ) ## just uses sys.exit
