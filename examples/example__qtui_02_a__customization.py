from joecceasy import Easy
from joecceasy import Easy

instructions = Easy.TrimAndTab(r"""
    ##
    Instructions:
    This is some instructional text.
    It can be multiple lines if you like.
""")

## Create and run a Qtui app with more customization
qtui = Easy.Qtui(
    title="Joecceasy Qtui  Example - Customization",
    tabTitle='DefaultTab',
    showInput=False,
    showInstructions=True,
    instructionsText=instructions,
)
exitCode = qtui.execQapp()
Easy.Exit( exitCode )