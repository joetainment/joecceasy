'''
Ipy - from joecceasy - EasyIpy

Classes to make working with IPython much easier, including EasyIpy


'''
from __future__ import print_function
import os, sys
import IPython
## for Ipy magic
from IPython.core.magic import (
  Magics, magics_class, line_magic,
  cell_magic, line_cell_magic
)
## for prompt
from IPython.terminal.prompts import Prompts, Token


## Get self mod and package __init__ mod (joecceasy modules)
## It is safe to get this without circular import problems
## because Qtui is only ever called 'lazily', after
## joecceasy module is fully loadedimport sys  ## just for SelfMod/SelfPak most imports later section
SelfPak=__import__(__package__)    
SelfMod=sys.modules[__name__]
joecceasy = SelfPak
from . import Utils
from .Utils import classproperty
from . import EasyMod
from . import Easy


class EasyIpy():
  """
  EasyIpy from joecceasy


  Config:
    c = get_config()
    from joecceasy import Easy
    Easy.Ipy.OnConfig( c ) ## c is from get_config()


  Startup:
    Reccommended use is something like below, in your .ipython profile startup folder in startup.py:

    from joecceasy import Easy
    Easy.Ipy.OnStartup(__name__)

    will auto populate useful var into ipython at startup!

  """
  @classmethod
  def  OnConfig(cls, config ):
      c = config
      c.InteractiveShell.autocall = 1
      c.TerminalInteractiveShell.prompts_class = JoeccIpyPrompt
      c.TerminalIPythonApp.display_banner = False

  @classmethod
  def  OnExit(cls, ):
      raise NotImplementedError
      ## not sure how to make this work since
      ## atexit runs at exit of ipy startup, not actual exit
      ## and ipython has no event for system exit
      ## most we can do is run after each command,
      ## which should be good enough to pass exit info into a file
      

  @classmethod
  def OnPostExecute(cls, ):
      #Easy.LogN( 50, 'Easy.Ipy exiting!')
      
      ## was for keeping track of last cwd
      file = os.environ.get( 'EasyIpyTempFileForTrackingCwd', '' )
      #Easy.LogN( 50,  file )
      if '/tmp.' in file or '\\tmp.' in file \
        and file!='':
          with open( file, 'w' ) as fh:
              fh.write( os.getcwd() )



  @classmethod
  def OnStartup(cls, modName ):
      """
      Run this from an ipython startup file
      from joexxeasy import Easy ; Easy.Ipy.Startup(__name__)
      modName is nameOfModCallingThis
      """
      import sys
      targetMod = sys.modules[ modName ]
      cls.StartupVarsInjectToMod( targetMod )
      EasyIpyMagics.RegisterMagics()
      
      cls.RegisterPostExecute()

  @classmethod
  def RegisterAtExit(cls):
      raise NotImplementedError
      ## see OnExit func comments/notes
      #import atexit
      #atexit.register( cls.OnExit, ) #*args, **kwargs)

  
  @classmethod
  def RegisterPostExecute(cls):
      ipy = IPython.get_ipython()
      ipy.events.register('post_execute', cls.OnPostExecute )

      
  @classproperty
  def SelfMod( cls ):
    return SelfMod
      
  @classproperty
  def Shell( cls ):
    return IPython.get_ipython()

  @classmethod
  def StartupVarsInjectToMod( cls, targetMod ):
      startupVars = {
          'SelfMod' : targetMod,
          'ipy': IPython.get_ipython(),
          'ez' : Easy,
          'M' : Easy.Mods,
          'K' : EasyIpyMagics.GetInstance(),
          'Xx' : EasyIpyMagics.GetInstance().xx,
          'Xi' : EasyIpyMagics.GetInstance().xi,
          'Hb' : EasyIpyMagics.GetInstance().hb,
          'Hh' : EasyIpyMagics.GetInstance().hh,
      }
      for var, value in startupVars.items():
          setattr( targetMod, var, value )


  @classmethod
  def PrintConfig(cls):
    pr = IPython.paths.locate_profile()
    c = Easy.JoinDir( IPython.paths.locate_profile(), 'ipython_config.py' )
    with open(c,'r') as fh:
        print( fh.read() )


  @classmethod
  def PrintProfile(cls):
    pr = IPython.paths.locate_profile()
    print( pr )

  @classmethod
  def PrintStartup(cls):
    pr = IPython.paths.locate_profile()
    print( pr )
    s = Easy.JoinDir( IPython.paths.locate_profile(), 'startup' )
    print( f's is: {s}' )
    l = Easy.LsAbs( s )
    print( l )
    for f in l:
      try:
        with open(f,'r') as fh:
               print( fh.read() )
        print( '\n\n\n\n' )
      except:
        Easy.PrintTraceback()



  @classmethod
  def PrintEasyIpyStartupMessage(cls):
    import os
    import IPython
    import sys
    if True:
      print( 'Startup location via: IPython.paths.locate_profile()' )
      print(
        os.path.join( *[
          IPython.paths.locate_profile(),
          'startup',
          'joecc-ipython-profile-default-startup.ipy',
        ])
      )
      print( "Vars are:     In (list)   Out (dict)   ipy (ipython)   ez (Easy)   m (Easy.Mods)" )
      print( "Paste lines of code via first using: %cpaste" )
      print( "Run system code (w aliases!)",
          "\n  via magic: %xx echo hey   or even:  xx echo hey ",
          "\n  or via python:   result=Xx('echo hey')",
          "\n     Xx works great with triple quoting over multi lines",
      )
      print( '################ EasyIpy ################' )





#### EasyIpyMagics
##
# The class MUST call this class decorator at creation time

                             #EasyIpyMagicsInstance_Workaround=None
@magics_class
class EasyIpyMagics(Magics):
    """
    Magics for EasyIpy because of custom init, they can hold additional state

    Actual magics are instance methods.
    """

    __Instance = None

    @classmethod
    def RegisterMagics( cls ):
        easyIpyMagics = cls.GetInstance( )
        IPython.get_ipython().register_magics(easyIpyMagics)

    @classmethod
    def GetInstance( cls ):
        if cls.__Instance is None:
            cls.__Instance = cls( IPython.get_ipython() )
        return cls.__Instance

    def __init__(self, shell, data=None):
        # You must call the parent constructor
        super(EasyIpyMagics,self).__init__(shell)
        self.data = data

    #### Actual magic instance methods ####
    @line_magic
    def hh(self, line=''):
        EasyIpy.PrintEasyIpyStartupMessage()

    @line_magic
    def hb(self, line=''):
        print( "\n\n\n########################################" )
        print( IPython.get_ipython().banner )
        EasyIpy.PrintEasyIpyStartupMessage()

    @line_magic
    def xx(self, line=''):
        """
            magic that works like %sx but allows aliases
              simplified since cells not needed
        """
        ## line in this context is one ipython line which may have line breaks in it
        line = self.xxFixLine(line)
        return self.shell.getoutput(line)

    @line_magic
    def xi(self, line=''):
        """ magic to call interactive commands like midnight-commander """
        #line = self.xxFixLine(line)
        return Easy.SubInteract( ['/bin/bash', '-i', '-c', line, ] ) #shell=True


    @line_cell_magic
    def xxCellExample(self, line='', cell=None):
        ## line in this p\case is one ipython line which may have line breaks in it
        line = self.xxFixLine(line)
        if cell is None:
            # line magic
            return self.shell.getoutput(line)
        else:
            opts,args = self.parse_options(line, '', 'out=')
            output = self.shell.getoutput(cell)
            out_name = opts.get('out', opts.get('o'))
            if out_name:
                self.shell.user_ns[out_name] = output
            else:
                return output

    #system = line_cell_magic('system')(sx)
    #bang = cell_magic('!')(sx)


    #### Non magic instance methods

    def xxFixLine(self, line):
        ## line in this context is one ipython line which may have line breaks in it
        line = "shopt -s expand_aliases \n source ~/.bash_aliases \n " + line
        return line



#### Custom Prompt
## Tokens of default prompt in ipy 5.0 are:
##   Prompt, PromptNum, OutPrompt and OutPromptNum.
class JoeccIpyPrompt(Prompts):
  #@classmethod
  #def RegisterToConfig( config ):


  def in_prompt_tokens(self, cli=None):
    return (
        ( Token.Prompt, 'In ['   ),
        ( Token.PromptNum, str(self.shell.execution_count)  ),
          
        ( Token.Prompt, '] '  ),
        ( Token.Prompt, os.getcwd()  ),
        ( Token.Prompt, " >>> "  ),
        
    )
  #def out_prompt_tokens(self, cli=None):
  #  return [(Token.OutPrompt ''), ]
  #def continuation_prompt_tokens(self, cli=None, width=None):
  #  return [(Token.Prompt, ''), ]
