from random import randint
import time

from joecceasy import Easy 

#from asciimatics.screen import Screen
#Screen = Easy.Ascui.AsciimaticsMod.screen.Screen

#Easy.Mods.sys.exit(  )

## Multiples can be used in sequence if you want multiple steps...

## First one, minor customization, no custom class
## note that since this functions as first screen only,
## we show "Next" instead of "Quit"
Easy.Ascui(title='Ascui Examples Step 1 of 2', quitLabel="Next", quitAskMsg='').exec_()

## Second one, via, customized subclass
class ExampleAscui( Easy.Ascui ):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
    def initWidgets(self):
        self.frame.createWidget("Text", "MyText", "My Text" )
        self.frame.createWidget("Divider", "Divider01", None, height=3 )
        
        self.frame.createWidget("Button", "Do Nothing", None, layoutCol=0, inFooter=True )
        self.frame.createWidget("Button", "Show Anim Msg", None,
            layoutCol=1, inFooter=True,
            callback=lambda:
              Easy.Ascui.FullscreenMsg(
                msg="Button was pressed!",
                timeout=1
              )
        )

exampleAscui = ExampleAscui(title='Ascui Examples Step 2 of 2')
exampleAscui.exec()
