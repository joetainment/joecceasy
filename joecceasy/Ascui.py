"""
Ascui - Easy UIs using Asciimatics
"""
import os, sys, time

## Get self mod and package __init__ mod (joecceasy modules)
## It is safe to get this without circular import problems
## because Ascui is only ever called 'lazily', after
## joecceasy module is fully loaded
SelfPak=__import__(__package__)    
SelfMod=sys.modules[__name__]
from .Utils import classproperty
import joecceasy
from . import EasyMod
from . import Easy
assert EasyMod.EasyModLoadingIsComplete==True


import asciimatics
import asciimatics.screen
## was only in git: import asciimatics.constants
import asciimatics.effects
import asciimatics.event
import asciimatics.exceptions
## was only in git: import asciimatics.parsers
import asciimatics.particles
import asciimatics.paths
import asciimatics.renderers
import asciimatics.scene
import asciimatics.screen
import asciimatics.sprites
import asciimatics.utilities
import asciimatics.widgets











from asciimatics.widgets import Frame, TextBox, Layout, Label, Divider, Text, \
    CheckBox, RadioButtons, Button, PopUpDialog, TimePicker, DatePicker, DropdownList, PopupMenu
from asciimatics.widgets import Background
from asciimatics.event import MouseEvent
from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, \
    InvalidFields
#from asciimatics.parsers import AsciimaticsParser
import sys
import re
import datetime
#import logging
#logging.basicConfig(filename="forms.log", level=logging.DEBUG)





GlobalExampleTreeString = r"""
       ${3,1}*
${2}      / \
${2}     /${1}o${2}  \
${2}    /_   _\
${2}     /   \${4}b
${2}    /     \
${2}   /   ${1}o${2}   \
${2}  /__     __\
  ${1}d${2} / ${4}o${2}   \
${2}   /       \
${2}  / ${4}o     ${1}o${2}.\
${2} /___________\
      ${3}|||
      ${3}|||
""".split("\n")








'''
class AscuiFrameOld(Frame):
    def __init__(self, screen, *args, **kwargs):
        #argsOrig = args  ## like tuple(args) because args is already a tuple
        #kwargsOrig = kwargs.copy()
        ## Defaults that will be applied to self
        ##   add specified entries from kwargs
        ##   or fallback defaults to self.
        self.parent = kwargs['parent']
        self.parent.frame = self        
        dkwargsForSelf = {
            #'parent': None,
            'widthRef': None,
            'heightRef': None,
            'layoutColumnWidths': [1,18,1],
            'nameRef': 'MyAscuiApp',
            'screenRef': screen,
            'hasShadowRef': True
        }
        Easy.DictOfDefaultsOntoObj( self, dkwargsForSelf, kwargs )
        
        ## Defaults that shouldn't get applied to self
        dkwargsLocal = {
        }
        Easy.DictOfDefaultsOntoDict( dkwargsLocal, kwargs )
        
        if self.heightRef is None:
            self.heightRef = int(screen.height * 9 // 10)
        if self.widthRef is None:
            self.widthRef = int(screen.width * 9 // 10)        

        super().__init__(
            screen,
            self.heightRef,
            int(screen.width * 9 // 10),
            data=self.parent.form_data,
            has_shadow=self.hasShadowRef,
            name=self.nameRef
        )
        self.widgets={}
        self.layouts = {}
        
        ## On_CHANGE triggers early, and needs reset, to this button must be made first
        self._reset_button = Button("Reset", self._reset)
        layout = Layout(  self.layoutColumnWidths ) #[1, 18, 1])
        
        self.add_layout(layout)
        ## layout add takes a widget and a column as args
        layout.add_widget(Label("Ascui Example App:"), 1)
        layout.add_widget(Divider(height=3), 1)
        """
        layout.add_widget(TextBox(5,
                                  label="My First Box:",
                                  name="TA",
                                  #parser=AsciimaticsParser(),
                                  line_wrap=True,
                                  on_change=self._on_change), 1)
        """
        self.exampleTextEdit = Text(label="Text",
                 name="Text",
                 on_change=self._on_change,
                  )
        layout.add_widget( self.exampleTextEdit, 1)
        layout.add_widget(
            Text(label="Alpha:",
                 name="TB",
                 on_change=self._on_change,
                 validator="^[a-zA-Z]*$"), 1)
        layout.add_widget(
            Text(label="Number:",
                 name="TC",
                 on_change=self._on_change,
                 validator="^[0-9]*$",
                 max_length=4), 1)
        """
        layout.add_widget(
            Text(label="Email:",
                 name="TD",
                 on_change=self._on_change,
                 validator=self._check_email), 1)
        layout.add_widget(Text(label="Readonly:", name="RO"), 1)
        """
        layout.add_widget(Divider(height=3), 1)
        #layout.add_widget(Label("Group 2:"), 1)
        """
        ## radio buttons mess up arrow baed nav,
        ## and require tab to nav since arrows choose
        layout.add_widget(RadioButtons([("Option 1", 1),
                                        ("Option 2", 2)],
                                       label="A Longer Selection:",
                                       name="RadioChoice",
                                       on_change=self._on_change), 1)
        """
        layout.add_widget(CheckBox("Field 1",
                                   label="A very silly long name for fields:",
                                   name="CA",
                                   on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 2", name="CB", on_change=self._on_change), 1)
        layout.add_widget(
            CheckBox("Field 3", name="CC", on_change=self._on_change), 1)
        """
        layout.add_widget(DatePicker("Date",
                                     name="DATE",
                                     year_range=range(1999, 2100),
                                     on_change=self._on_change), 1)
        """
        """
        layout.add_widget(
            TimePicker("Time", name="TIME", on_change=self._on_change, seconds=True), 1)
        layout.add_widget(Text("Password", name="PWD", on_change=self._on_change, hide_char="*"), 1)
        """
        layout.add_widget(DropdownList(
            [("Item 1", 1),
             ("Item 2", 2),
             ("Item 3", 3),
            ],
            label="Dropdown", name="DropDownChoice", on_change=self._on_change), 1)
        layout.add_widget(Divider(height=3), 1)

        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
                
        #layout2.add_widget(self._reset_button, 0)
        ## Buttons takes args as stringFor Label, callback
        #layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("ExampleButton", self.onExampleButton), 0)
        layout2.add_widget(Button("Quit", self._quit), 2)
        print("self.fix()")
        self.fix()

    def update(self, frame_no):
        super().update(frame_no)
        ## note that updates are trigged by effects/widgets
        ## on changes and by timer (frame_update_count) when
        ## there are no changes
        print( f'u:{frame_no} ',end='')

    def process_event(self, event):
        # Handle dynamic pop-ups now.
        if event is not None  and  isinstance(event,KeyboardEvent ):
           if event.key_code == ord('q'):
               print( ' q pressed! ')   
           if event.key_code == Screen.KEY_ESCAPE:
               print( ' esc pressed! ')
               raise StopApplication("User requested exit")   
        elif (event is not None and isinstance(event, MouseEvent) and
                event.buttons == MouseEvent.DOUBLE_CLICK):
            # By processing the double-click before Frame handling, we have absolute coordinates.
            options = [
                ("Default", self._set_default),
                ("Green", self._set_green),
                ("Monochrome", self._set_mono),
                ("Bright", self._set_bright),
            ]
            if self.screen.colours >= 256:
                options.append(("Red/white", self._set_tlj))
            self._scene.add_effect(PopupMenu(self.screen, options, event.x, event.y))
            event = None

        # Pass any other event on to the Frame and contained widgets.
        return super().process_event(event)


    def _on_change(self):
        changed = False
        self.save()
        for key, value in self.data.items():
            if key not in self.parent.form_data or self.parent.form_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed

    def onExampleButton(self):
        
        print(f"Button Pushed! {self.data['Text']}")
        #self.screen.redraw()
        ## updating widgets in code isn't working yet
        #self.data['Text'] = self.exampleTextEdit = 'New Text'

    def _reset(self):
        self.reset()
        raise NextScene()

    def _view(self):
        # Build result of this form and display it.
        try:
            self.save(validate=True)
            message = "Values entered are:\n\n"
            for key, value in self.data.items():
                message += "- {}: {}\n".format(key, value)
        except InvalidFields as exc:
            message = "The following fields are invalid:\n\n"
            for field in exc.fields:
                message += "- {}\n".format(field)
        self._scene.add_effect(
            PopUpDialog(self._screen, message, ["OK"]))

    @staticmethod
    def _check_email(value):
        m = re.match(r"^[a-zA-Z0-9_\-.]+@[a-zA-Z0-9_\-.]+\.[a-zA-Z0-9_\-.]+$",
                     value)
        return len(value) == 0 or m is not None

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")
'''


class ReturnInfo():
    def __init__(self, value=None, exitCode=None, maker=None ):
                                      #  #  *args, **kwargs):
        """
           maker is most often going to be self in scope that called init
           but it must be explicitly passed
        """
        self.value = value
        self.exitCode = exitCode
        self.maker = maker

    @classproperty        
    def asTuple(self):
        return  self.value, self.exitCode,  self.maker,
    @classproperty
    def asDict(self):
        return {
            'value':self.value,
            'exitCode':self.exitCode,
            'maker':self.maker,
        }
    

class ReturnPopper( ):

    def __init__(self):
        self.initReturnPopper()

    def initReturnPopper(self):
        self._returns = ( )
            
    def returnsPeek(self, index=None):
        if index is None:
            if len(self._returns)>0:
                return self._returns(-1)
            else:
                return None
        else:
            return self._returns[ index ]

    def returnsPop(self, index=None):
        if index is None:
            if len(self._return)>0:
                return self._returns.pop()
            else:
                return None
        else:
            return self._returns.pop(index)


    def returnsPush(self, info=None, index=None):
        if index is None:
            self._returns.append(info)
        else:
            self._returns.insert( index, info )

    def returnsPut(self, info=None, index=None):
        if index is None:
            if len(self._returns)>0:
                self._returns[-1] = info
            else:
                self._returns.append( info ) 
        else:
            self._returns[index] = info

    

    
class Chainable( ReturnPopper ):
    def __init__(self):
        self.initChainable()

    def initChainable(self):
        super().__init__()
        
    def chain(self, action, args=(), kwargs={}, actionReturnsExitCode=False ):
        """
        allows performing an action but returning self
        store the return value at end of self._returns, which can be gotten after via self.returnsPop()
        """
        objToCall = getattr( self, action )
        exitCode = None
        result = objToCall(*args,**kwargs)
        if actionReturnsExitCode:
            exitCode = result
            resultValue = None
        else:
            exitCode = None
            resultValue = result
            
        returnInfo = ReturnInfo( value = resultValue, exitCode=resultExitCode )
        self.returnsPush( returnInfo ) 
        return self

    def chain2(self, action, args=(), kwargs={}, ):
        """
        allows performing an action and returning   2 item tuple of   resultValue, self
        """
        if not isinstance( action, str):
            objToCall=action
        else:
            objToCall = getattr( self, action )
        result = objToCall(*args,**kwargs)
        #returnInfo = ReturnInfo( value = result )
        #self.returnsPush( returnInfo ) 
        return value, self

    def chain2Info(self, action, args=(), kwargs={}, actionReturnsExitCode=False ):
        """
        allows performing an action and returning  tuple of  resultInfo, self
        """
        if not isinstance( action, str):
            objToCall=action
        else:
            objToCall = getattr( self, action )
        result = objToCall(*args,**args)
        resultInfo = ReturnInfo( value = result, exitCode=None ) 
        return reultInfo, self

    def chain3(self, action, args=(), kwargs={}, actionReturnsExitCode=False ):
        """
        allows performing an action but returning   3 item tuple of   resultValue, resultExitCode, self
        """
        if not isinstance( action, str):
            objToCall=action
        else:
            objToCall = getattr( self, action )
        result = objToCall(*args,**kwargs)
        if actionReturnsExitCode:
            resultValue = result
            resultExitCode = None
        else:
            resultValue = None
            resultExitCode = result
        return resultValue, resultExitCode, self



class AscuiFrame(Frame):
    def __init__(self, screen, *args,
        parent=None, callbackOnChange=None,
        quitAskMsg="Quit? Are you sure?",
        **kwargs,
        ):
        """
        
        quitAskMsg can be set to blank in order to not ask at all
        
        self.widgets and self.layouts are dicts
        default layout is named "DefaultLayout"
        
        Theme can be set using:
            self.set_theme("default")
            self.set_theme("green")
            self.set_theme("monochrome")
            self.set_theme("bright")
            self.set_theme("tlj256")
            maybe more depending on what super()'s Frame supports
        """
        ## these kwargs will get passed to super, Frame
        #dkwargsForSelf = {
        #            'frameData':{}
        #}
        #Easy.DictOfDefaultsOntoObj( self, dkwargsForSelf, kwargs )        
        if 'data' not in kwargs:
            kwargs['data']={}
            
        self.defaultLayoutColumnWidths = [1, 18, 1]
        self.defaultFooterLayoutColumnWidths = [1, 1, 1]
        self.quitAskMsg=quitAskMsg
        self.parent=parent,
        
        self.callbackOnChange = callbackOnChange
        super().__init__(screen, *args, **kwargs )
        
        if not hasattr( self, "widgets" ):
            self.widgets={}
        if not hasattr( self, "layouts" ):
            self.layouts={}
            
        self.createLayout('DefaultLayout', self.defaultLayoutColumnWidths)
        self.createLayout('DefaultFooterLayout', self.defaultFooterLayoutColumnWidths )
        
    def process_event(self, event):
        # Handle dynamic pop-ups now.
        evIsEscKey = (     event is not None
                       and isinstance(event,KeyboardEvent )
                       and event.key_code == Screen.KEY_ESCAPE )
        if evIsEscKey:
               #print( ' esc pressed! ')
               self.quitWithoutAsk()
               #raise StopApplication("User requested exit")
        else:
            try:
                super().process_event( event )
            except StopApplication:
                raise
            except KeyboardInterrupt:
                raise
            except:
                print( Easy.Mods.traceback.format_exc() )
                print("An event could not be processed.")
                print(
                    "You may want to look into the AscuiFrame.process event code"
                )
                raise

    def createLayout(self, name,
            layoutColumnWidths=None, autoAdd=True
        ):
        if layoutColumnWidths is None:
            layoutColumnWidths=self.defaultlayoutColumnWidths
        self.layouts[name]= layout = Layout( layoutColumnWidths )
        if autoAdd==True:
            self.add_layout( layout )
        return layout
        
    def createQuitButton(self, layout=None, label="Quit", inFooter=False):
               #if layout is None:
               #    layout=self.layouts['DefaultLayout']
               #if not isinstance(layout, Layout):
               #    ## at this point it's not a Layout or None,
               #    ## so we can try it as a string, which either works or its an error
               #    layout = self.layouts[ layout ]
        ## we just pass layout directly since createWidget can figure it out
        if self.quitAskMsg=='':
            cb=self.quitWithoutAsk
        else:
            cb = self.quitWithAsk 
        return self.createWidget(
            "Button", "QuitButton", label,
            callback= cb,
            layout=layout,
            inFooter=inFooter,
        )
        
            
    def createWidget(self,
            kind,
            name,
            val,                      
            *args,
            label=None,
            callback=None,
            layout=None,
            layoutCol=1,
            inFooter=False,
            **kwargs ):
        """
        param: layout - layout object or dict key
        examples:
        self.frame.createWidget( "Divider", "Divider02", "", height=3)
        self.frame.createWidget( "Label", "ExampleLabel", "Example Label " )
        self.frame.createWidget( "Text", "ExampleText", "some text", label="Example Text ")
        self.frame.createWidget( "TextBox", "ExampleTextBox", "some text \n next line".split('\n'), label="Example Text ")
        self.frame.createWidget( "Button", "Button01", None, label="PushMeButton", callback=onButton01)
        self.frame.createWidget( "Button", "Button02", "ButttonsCanPassValToBeLabelInsteadofLabelKeyword", callback=onButton02)
        """
        assert name not in self.data

        if label==None:
            if kind=="Button":
                if isinstance(val,str):
                    label=val
                else: label=name
            else:
                label=name
        else:
            label=name
            
        if kind=='Text':
            ## val isn't included in call because in comes from data
            self.data[name]=val
            if callback is None:
                callback=self.on_change
            widget=Text( *args,
                name=name, label=label, on_change=callback, **kwargs )
        elif kind=="Label":
            widget=Label( val, *args, **kwargs )
        elif kind=="Button":
            if callback is None:
                callback=lambda: None
            widget=Button( label, callback, *args, **kwargs )
        elif kind=="Divider":
            widget=Divider( *args, **kwargs )
        elif kind=="TextBox":
            if isinstance(val,str):
                val = val.split('\n')
            self.data[name]=val
            if callback==None:
                callback=self.on_change            
            textBoxHeight=kwargs.get('height',3)
            if 'height' in kwargs:
                del kwargs['height']
            widget = TextBox(textBoxHeight,
                label=label,
                name=name,
                #parser=AsciimaticsParser(),
                on_change=callback, *args, **kwargs)
        else:
            raise Exception('incorrect kind arg given')
        self.widgets['name']=widget
        if layout is None:
            if inFooter==True:
                layout=self.layouts['DefaultFooterLayout']
            else:
                layout=self.layouts['DefaultLayout']
        if not isinstance(layout, Layout):
            layout = self.layouts[ layout ]
        layout.add_widget( widget, layoutCol )
        return widget    
            
    def on_change(self):
        #changed = False
        self.save()
        if self.callbackOnChange is not None:
            self.callbackOnChange() #parent.on_change
        #for key, wg in self.widgets.items():
        #    wg.refresh()
        #for key, ly in self.layouts.items():
        #    ly.update_widgets()   ##refresh()
        #self.update_widgets()
        
        """
        for key, value in self.data.items():
            if key not in self.parent.form_data or self.parent.form_data[key] != value:
                changed = True
                break
        self._reset_button.disabled = not changed
        """
        
    def modalPopup(self,
        msg='Please choose a choice',
        choices=["Choice Zero", "Choice One"],
        callback=lambda choice:None,
        has_shadow=True,
        ):
        self.scene.add_effect(
            PopUpDialog(self.screen,
                msg, choices,
                has_shadow=has_shadow,
                on_close=callback
            )
        )

    def quitWithAsk(self, ):  #returnInfo=None, returnExitCode=0 ):
        #print( arg )
        #print( type(arg) )
        #raise StopApplication( msg )
        #self.scene.exit()
        #self.screen.close(True)
        #return
        quitChoiceCallback = self.quitIfChosen
        #raise KeyboardInterrupt()
        #raise StopApplication( "quitting via StopApplication" )
        self.modalPopup(
            msg=self.quitAskMsg,
            choices=['Yes','No'],
            has_shadow=True,
            callback=quitChoiceCallback
        )
        
    def quitIfChosen( self, choice ):
            #print( f'choice: {choice}' )
            if choice==0:
                self.quitWithoutAsk()
    

    def quitWithoutAsk(self, *args, msg='Quitting App'):
        raise StopApplication( msg )
          ## this was failing because an int was gettting passed in
          ## as positionalKeyword args, so now it can only be passed in as keyword
                



    
        
class Ascui(Chainable ):
    """
        Gnerally if you pass a data dict to thi class it works best
    """
    @classproperty
    def SelfMod(cls):
        return SelfMod
    
    @classproperty
    def AsciimaticsMod(cls):
        return asciimatics
    
    @classmethod
    def FullscreenMsg( cls, timeout=3, msg=None, showCountdown = True ):
        def fullscreenMsgLocal(screen):
            nonlocal msg
            if msg is None:
                msg = f'Press Q to exit'
            startTime=time.time()
            remainTime = startTime + timeout - time.time()
            #remainTimeAsInt = Easy.Mods.math.
            msgCombined = msg
            while remainTime > 0:
                remainTime = max(startTime + timeout - time.time(), 0)
                r1 = Easy.Mods.random.randint(0, screen.width)
                r2=Easy.Mods.random.randint(0, screen.height)
                rc=Easy.Mods.random.randint(0, screen.colours - 1)
                rb=Easy.Mods.random.randint(0, screen.colours - 1)
                screen.print_at(msg,
                                r1, r2,
                                colour=rc,
                                bg=rb)
                if showCountdown:
                    screen.print_at( f'{remainTime} second left...',0,0)
                ev = screen.get_key()
                if ev in (ord('Q'), ord('q')):
                    return
                screen.force_update()
                screen.refresh()
                time.sleep(0.1)
                screen.refresh()
        Screen.wrapper(fullscreenMsgLocal)
    
    
    def __init__(self, *args,**kwargs):
        dkwargsForSelf = {
            'title' : "Ascui App",
            'data':{},
            'name':None,
            'exitCode': 0,
            'theme':None,
            'autoExampleWidgets':True,
            'quitLabel' : 'Quit',
            'quitIsAtTop' : False,
            'parent' : None,
            'quitAskMsg' : 'Quit? Are you sure?',
        }
        Easy.DictOfDefaultsOntoObj( self, dkwargsForSelf, kwargs )                 

        #self.lastReturnInfo = None

        self.initChainable()
        
        #self.returns = []
        
        if self.name is None:
            self.name=self.title.replace(' ', '') 
        
        self.screen = Screen.open( )
        
        self.frameWidth = int(self.screen.width * 9 // 10)
        self.frameHeight = int(self.screen.height * 9 // 10)
    
        
    

        ## AscuiFrame is subclass of frame but auto exits on esc
        self.frame = AscuiFrame(
            self.screen,
            self.frameHeight,
            self.frameWidth,
            ## frame can auto create its data dict, but it's
            ## better to pass our own in
            parent=self,
            data=self.data,
            has_shadow=False, #was self.hasShadowRef,
            name=self.name,
            quitAskMsg=self.quitAskMsg,
        )
        self.data = self.frame.data ## this is kinda redundant now
        if self.theme is not None:
            self.frame.set_theme(self.theme)

        self.background = Background(self.screen)
        
        #self.widgets={}
        #self.layouts = {}        
        #self.layouts['default'] =
        
        #self.layout = self.frame.layouts["DefaultLayout"]
            #Layout(  self.layoutColumnWidths ) #[1, 18, 1])
           
        self.frame.createWidget("Label", "AppTitle", self.title )
        if self.quitIsAtTop==True:
            self.frame.createQuitButton(label=self.quitLabel, inFooter=True)
            self.frame.createWidget( "Divider", "Divider01", "", height=3)
        
        self.initWidgets()

        if self.quitIsAtTop==False:
            #self.frame.createWidget( "Spacer", height=1, inFooter=True)
            self.frame.createWidget( "Divider", "Divider01", "", height=3,inFooter=True)
            self.frame.createQuitButton(label=self.quitLabel, inFooter=True)
        
        ## Frame is a subclass of Effect, and Scenes are collections of effects 
        self.scene = Scene([
            self.background,
            self.frame,             
        ],-1) ## what is the -1 for? investigate
        
    
    def run(self):
        returnInfo = AscuiReturnInfo(parent = self,
        exitCode = self.exec_(),
        value = self.lastReturnValue )
        return self, exitCode, value
    
    def exec(self):
        return self.exec_()

    def exec_(self):           
        #return AscuiFrame.Exec( parent=self ) ##last_scene=None - karg
                
        #### Update loop, freq of updates controlled by frame_update count
        #### properties returned by widgets, generally every fifth frame
        #### for Text UI that isn't animated. Widget state changes als
        #### trigger updates
        ## note, scene will stop playing if StopApplication is raised
        ## explicit exception handling of StopApplication isn't required
        self.frame.fix() ## Call fix just before playing
        try:
            self.screen.play(
                [self.scene, ], ## takes a list of scenes
                stop_on_resize=True, start_scene=self.scene, allow_int=True,
            )
        except KeyboardInterrupt as err:
            print("Ascui stopped by KeyboardInterrupt (e.g. ctrl-c )" )
        except StopApplication as err:
            print("Ascui stopped by StopApplication" )
        
        self.screen.close(restore=True)
        return self.exitCode
    
    def initWidgets(self):
        """
        Override this to make your own widgets
        """
        if self.autoExampleWidgets:
            self.initExampleWidgets()
    
    def initExampleWidgets(self):
        self.frame.createWidget( "Label", "ExampleLabel", "Example Label " )
        self.frame.createWidget( "Text", "ExampleText",
                        "some text", label="Example Text ")       

        self.frame.createWidget( "Divider", "Divider01", "", height=3)
        self.frame.createWidget( "TextBox", "Example TextBox", " text editor \n press tab \n to change focus",
            height=3, line_wrap=True)
        
        def onExampleButton():
            self.frame.modalPopup( msg="Example Button Pressed!", choices=['OK'] )

        self.frame.createWidget( "Divider", "Divider01", "", height=3 )
        self.frame.createWidget( "Button",
            "ExampleButton01", "Push me!",
            callback=onExampleButton,
            inFooter=True,
            layoutCol = 0,
        )
        self.frame.createWidget( "Button",
            "ExampleButton02", "Do Nothing",
            inFooter=True,
            layoutCol = 1,
        )        
        


'''
def oldDisabledCodeWasInAscuiFrameClass():
    
    @classmethod
    def Exec(cls, *args, last_scene=None, **kwargs):
        def defaultCallback(*args,**kwargs):
            return {'continueExecLoop':True}
        callback = kwargs.get( 'callback', defaultCallback )
        callbackArgs = kwargs.get( 'callbackArgs', tuple() )
        callbackKwargs = kwargs.get( 'callbackKwargs', {} )
        ## not entirely sure why this is a loop
        while True:
            callbackResult = callback( *callbackArgs, **callbackKwargs )
            continueExecLoop = callbackResult['continueExecLoop']
            print ( Easy.Mods.time.time() )
            if not continueExecLoop:
                break
            return cls.ScreenWrapperCall( last_scene, *args,**kwargs )

                
    @classmethod
    def ScreenWrapperCall(cls, last_scene, *args, **kwargs):
        try:
            ## The call below is structured pretty strangely
            ## because we can't alter the internals of Screen.Wrapper
            ## our args and kwargs are sneaked into its arguments list
            exitCode = Screen.wrapper(
                cls.FuncForScreenWrapperToUse,
                catch_interrupt=False,
                ## *,** left out on purpose
                arguments=[last_scene,args,kwargs] 
            )
            print( f"exitCode is: {exitCode}" )
            return exitCode #self.exitCode
        except ResizeScreenError as e:
            last_scene = e.scene        
    
    ## The way the asciimatic library works is pretty weird
    ## so this function and its args/kwargs are pretty weird because
    ## they are setup in a way that lets the Screen.Wrapper function
    ## indirectly trigger this function getting called
    @classmethod
    def FuncForScreenWrapperToUse(cls, screen, scene , args , kwargs ):
        ## avoid maxing out CPU, 
        ## even at 0.03 cpu load may be ~1%
        time.sleep(0.03) 
        screen.play([Scene([
            Background(screen),
            #self,
            cls(screen, *args,**kwargs)#args, kwargs)
        ], -1)], stop_on_resize=True, start_scene=scene, allow_int=True)
        #return self.exitCode ## no self in this func implementation
        #print( "exitCode hardcoded to zero")
        return 0 ## exit code, not properly implemented yet, hardcoded to zero
'''
        
"""        
        # Test data
        self.tree = GlobalExampleTreeString

        # Initial data for the form
        self.frameData = {
            "TA": self.tree,
            "Text": "Example Text",
            "TB": "alphabet",
            "TC": "123",
            "TD": "a@b.com",
            "RO": "You can't touch this",
            "RadioChoice": 2,
            "CA": False,
            "CB": True,
            "CC": False,
            "DATE": datetime.datetime.now().date(),
            "TIME": datetime.datetime.now().time(),
            "PWD": "",
            "DropDownChoice": 1
        }
"""        
        

