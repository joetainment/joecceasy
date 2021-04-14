from joecceasy import Easy

instructions = "Instructions: " \
"This is some instructional text. It can be multiple lines if you like. " \
"Click Go to get a message!\n"

def onGoButtonClicked():
    global qtui
    qtui.print( "Go button was clicked at epoch time: " \
        f"{Easy.Mods.time.time()}" )    

qtui = Easy.Qtui( title="JoecceasyQtuiExample",
    instructionsText = instructions,
    showInput=False,
    callbacks = { 'onGoButtonClicked': onGoButtonClicked },
)
exitCode = qtui.execQapp() ## qtui.qapp.exec_() would do the same
Easy.Exit( exitCode ) ## just uses sys.exit
