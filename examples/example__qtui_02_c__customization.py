from joecceasy import Easy
from joecceasy import Easy

instructions = Easy.TrimAndTab(r"""
    ##
    Instructions:
    This is some instructional text.
    It can be multiple lines if you like.
""")

def additionalWidgetsInMain( qtui ):
    qw = qtui.QtWidgets
    qtui.mainLayout.addRow(
        qw.QLabel( 'This is an added row in main!'),   
        qw.QPushButton('click me'),
    )
def additionalWidgetsInPre( qtui ):
    qw = qtui.QtWidgets
    qtui.mainLayout.addRow(
        qw.QLabel( 'This is an added row, before!'),   
        qw.QPushButton('click me'),
    )
def additionalWidgetsInPost( qtui ):
    qw = qtui.QtWidgets
    qtui.mainLayout.addRow(
        qw.QLabel( 'This is an added row, after!'),   
        qw.QPushButton('click me'),
    )

## Create and run a Qtui app with more customization
qtui = Easy.Qtui(
    title="Joecceasy Qtui  Example - Customization",
    tabTitle='DefaultTab',
    showInput=False,
    showInstructions=True,
    instructionsText=instructions,
    callbacks = {
        'initAdditionalWidgetsIntoDefault': additionalWidgetsInMain,
        'initWidgetsPre': additionalWidgetsInPre,
        'initWidgetsPost': additionalWidgetsInPost
    },
)
exitCode = qtui.execQapp()
Easy.Exit( exitCode )