r"""
joecceasy python package __init__.py

Recommended way of importing, without magic, is:
from joecceasy import Easy
from joecceasy import *

Recommended way of importing, with magic, is:
from joecceasy import Easy; exec(Easy.CodeQ); exit(); #%exit


Note, as a general rule, lowercase is only used for
local vars in functions, funcs in functions instance methods
(regular methods of classes) or module level vars
that aren't intended to be used outside the module.
Classes, and externally useful var and funcs


to do:
  add option to cd to script dir
    gather other useful info
  FileInfo class to gather or generate useful info/attr of files/path
    like abs, PathWasRelativeToThisOtherPath, etc
  ArgsParse needs feature to parse from string
    the instance should have a parseFromString option
    which if not None, is used instead of sys.argv
  consider adding libs like fastcore, NestedText
  pprint and colorama options
  run commands super easy and get back output and errors easy
  chain funcs, make more general prupose chainable class in Utils
  CiDict should use a twin dict system so that it can remember the
  case of original keys, but get and choose replace by lower keys only
  
  
  make it easy to escape args list for cmd line call
    even with shell=True
      subprocess.list2cmdline  on windows
      shelx.join
  
      make function to quote if contains space, else
      windows ver will work different due to
      backslashes being escaped on unix
      can probably use shelx on linux 


Highlights:
  Easy.ArgsE    enumerated arguments iterator!
  Easy.ArgsCount
    both above only have args to your script, not script itself    

  Easy.ExtendBuiltinClass(str, extension_method )
    works if method takes self, uses "forbidden fruit" module    

  Easy.Cwd  same as os.getcwd()
  Easy.OrigWorkDir
  Easy.ScriptDir
  Easy.Chdir( )
  
  Easy.Init()  gives default easy options like chdir to scriptDir
    Otherwise, can use Easy().init()
    Init won't get called automatically
    This is to keep "static behavior"
    Avoid doing anything prior to being called.


  Easy.Fstring - For Using "late" F-Strings:
    exampleToFormat = "example number is: {number}"  ## no subs yet
    number = 1  ## now number is defined, late
    result = eval( Easy.Fstring( exampleToFormat ) )

  Easy.PrintWithFormat .PrintWithFormatV .Format .FormatV  
    r = Easy.PrintWithFormat( exampleToFormat, **locals() )
    ## or, substituting named filed with given value..
    r = Easy.PrintWithFormat( exampleToFormat, number=2 )
    number = 3
    ## alternate methods of doing the same, with optional end
    r = Easy.PrintWithFormatV( exampleToFormat, kwargs=locals(), end='\n\n\n' )
    # we don't have to print the results
    unprinted = Easy.Format( exampleToFormat, number=4 )
    # or
    substitutions={ 'number': 5}
    unprinted = Easy.FormatV( exampleToFormat, kwargs=substitutions )
    # or without, keyword arguments
    unprinted = Easy.FormatV( exampleToFormat, None, substitutions )
  
  
  Easy.TrimAndTab(r'''
      ###
      First Hashes and lines above and last line
      are trimmed and unindented.
      They can end (from a practical perspective)
      with windows backslashes too!
      e.g. C:\Windows\
  ''')  

  
"""
##################################################
##################################################


__all__ = ['Easy']  ## what to import on: from ThisModule import *

##################################################
###### SelfModReference
import sys  ## just for SelfMod/SelfPak most imports later section
SelfPak=__import__(__package__)    
SelfMod=sys.modules[__name__]
## can be used to run other code at loading complete
## to avoid circular import problems
SelfModLoadingCompleteCallbacks = []
## this can be checked to prevent circular imports
EasyModLoadingIsComplete=False


##################################################
##################################################
###### Imports

#################################
#### Python Standard Library imports
####
#import atexit, collections, datetime, importlib, inspect
#import os, sys, subprocess, time, tempfile, traceback
#from _ctypes import ArgumentError

#################################
#### joeceasy module imports
####  as a general rule, import the entire module first
####  and then optionally import explicit parts from it
from . import Utils
from . import Utils as UtilsMod
from .Utils import callInitCls, classproperty, Funcs, Object
from .Utils import EasyReturnedTimeout
from .EasyThread import EasyThread
from .FileWatcher import FileWatcher
from .AbstractBaseClass import AbstractBaseClass
from . import ModulesLazyLoader

#from . import EasypathBase
    
### Disabled and should probably be deleted later
##    since it done in metaclass instead
## forbiddenfruit.curse for extension
##   of built in classes
# from .submodules import forbiddenfruit

#### Configuration more likely to be modified
try:
    reload( EasyConf )
except:
    from . import EasyConf


#### end of imports (non-dynamic ones at least)
##################################################
##################################################

###############################################
###############################################
######## Globals from separate easy to edit file
EasyConf = Funcs.DirToObj( EasyConf )

###############################################
###############################################
## raw functions,  that can't work as def in class
## ----  none currently, all moved to .Utils ----


#################################
#### Easy metaclass and actual class
####

class EasyMeta(type):
    """
    Metaclass, mostly to enable class properties that can have both
    getters and setters
    """
    @property
    def EasyModLoadingIsComplete(cls):
        global EasyModLoadingIsComplete
        return EasyModLoadingIsComplete
    @EasyModLoadingIsComplete.setter
    def EasyModLoadingIsComplete(cls, v):
        global EasyModLoadingIsComplete
        EasyModLoadingIsComplete = v
    @property
    def P(cls):
        return getattr( cls, '_P', None)
    @P.setter
    def P(cls, v):
        setattr( cls, '_P', v )
        #print( v )
    def P_Clear(cls):
        delattr( cls, '_P')    


    @property
    def Ascui( cls ):
        from . import Ascui
        return Ascui.Ascui
    @property
    def Curse(cls):
        ## returns the curse function
        from .submodules import forbiddenfruit
        return forbiddenfruit.curse
    @property
    def Curses(cls):
        ## returns the decorator to curse a function
        from .submodules import forbiddenfruit
        return forbiddenfruit.curses
    @property
    def ForbiddenFruit(cls):
        from .submodules import forbiddenfruit
        return forbiddenfruit
    @property
    def Forbiddenfruit(cls):
        from .submodules import forbiddenfruit
        return forbiddenfruit
    
    @property
    def Ic( cls ):
        return Utils.ic
    @property
    def IcecreamIc( cls ):
        return icecream.ic
    @property
    def IcecreamIcc( cls ):
        return icecream.icc
    
    @property
    def Qtc( cls ):
        import PySide2.QtCore
        return PySide2.QtCore
    @property
    def Qtg( cls ):
        import PySide2.QtGui
        return PySide2.QtGui
    @property
    def Qtw( cls ):
        import PySide2.QtWidgets
        return PySide2.QtWidgets
    @property
    def Qtui( cls ):
        from . import Qtui
        return Qtui.Qtui    
    @property
    def QtuiExec( cls ):
        from . import Qtui
        return Qtui.Qtui.Exec
    @property
    def See(self):
        return Utils.see

    @property
    def Sultan(self):
        ## sultan - module for make subprocess and cmd line stuff easier
        from .submodules.sultan import Sultan
        return Sultan
    
    @property
    def Tubprocess(self):
        from . import Tubprocess
        return Tubprocess.Tubprocess
        
    @property
    def Unipath(self):
        from .submodules.unipath import Path
        return Path
        
    @property
    def UnipathMod(self):
        from .submodules import unipath as unipathMod
        return unipathMod
        
    
    ## This will run when the class is declared,
    ## just after the class block completes
    def __init__(selfCls, other1, other2, other3):
        #print( "Easy Class init!")
        selfCls._InitCls()
        
class Easy( metaclass=EasyMeta ):
    """
    Easy - joeceasy module's main class
    """
    ################################
    ######## Private Fields ########    
    ## the global easy access Singleton of the class, also @cls.Inst
    __SingletonInstance = None
    __ReloadCount = 0
    __ReloadStr = EasyConf.ReloadStr
    
    __Global = None



    ###################################
    #### Class and static methods
    @classmethod
    def _InitCls(cls):
        """
        This function should do nothing other than assemble the class itself.
        Don't do anything else that would trigger code other to run at
        class declaration time.
        """
        ## class body cody will have already run by the time it gets to here
        #print( cls.__dict__ )
        'pass'
    
    @classmethod
    def _SetReloadCount( cls, count ):
        cls.__ReloadCount = count 

    @classproperty
    def AbsPath(cls):
        return Funcs.AbsPath
    @classproperty
    def AbstractBaseClass(cls):
        return AbstractBaseClass
    
            
    
    @classmethod
    def AddClsMethods(cls, methods):
        cls.AddMethodsTo(obj, methods)
        return cls
        
    @staticmethod
    def AddMethodsTo(obj, methods):
        for i in methods:
            #print (i.__dict__)
            iname= i.__name__
            if hasattr(i, "ToBeStaticMethod"):
                if getattr(i,"ToBeStaticMethod"):
                    i=staticmethod(i)
                    i.__name__=iname
            #print( i )
            setattr(obj, iname, i)
        return obj    
    
        
    @classproperty
    def Argv0(cls):
        return cls.Inst.argv0
        
    @classproperty
    def Arg0(cls):
        return cls.Inst.argv0
        
    @classproperty
    def Arg(cls):
        """ just in case of typo return sam    e as Easy.Args"""
        return Funcs.Args
    @classproperty
    def Args(cls):
        return Funcs.Args
        
    @classproperty
    def ArgsCount(cls):
        return Funcs.ArgsCount
        
    @classproperty
    def ArgCount(cls):
        return Funcs.ArgsCount
    
    @classproperty
    def ArgsE(cls):
        return cls.EnumArgs()
    
    @classproperty
    def ArgsParser(cls):
        from . import ArgsParser
        return ArgsParser.ArgsParser
    
    @classproperty
    def ArgsAsOpts(cls):
        return Funcs.ArgsAsOpts
    
    @classproperty
    def ArgsToOpts(cls):
        return Funcs.ArgsToOpts
    
    @classproperty
    def Argv(cls):
        import sys
        return sys.argv

    @classproperty
    def Attrs(cls):
        return Easy.Mods.attrs
    
    @classproperty
    def AttrsDef(cls):
        return Easy.Mods.attrs.define
    
    @classproperty
    def AttrsField(cls):
        import attrs
        return Easy.Mods.attrs.field
                
    @classmethod
    def Call( cls, *args, **kwargs ):
        return cls.CallActual( *args, **kwargs )

    @classmethod    
    def CallActual(self, argsForCommandLine, magicDict=None, quiet=False, loud=False, interactive=False, doMagic=True, autoEscape=False):
        """
        """
        import subprocess
        
        if magicDict!=None and doMagic:
            if autoEscape:
                raise "auto escape in Easy Call functions can't be used together with Call Magic"
            if not isinstance( argsForCommandLine, str ):
                "Call magic only works with a single string used as the command line"
            for k, v in magicDict.items():
                mkey = '#%' + k + '%#'
                if mkey in argsForCommandLine:
                    argsForCommandLine = (
                        argsForCommandLine.
                            replace(
                                mkey,
                                str(v)
                            )
                        ,
                    )
                #print( argsForCommandLine )
        #print( argsForCommandLine )
        
        if autoEscape:
            if isinstance(args, str):
                raise "autoEscape only works with lists of args, and each arg will be escaped separately"
            raise "autoEscape not yet implemented, use one of the Easy.EscArgs functions instead"
            #argsForCommandLine = cls.EscArgForCmdExe(argsForCommandLine)
            

        
        if not quiet:
            if loud==True:
                print( '-------- Before Start of Call --------' )
                if not isinstance( argsForCommandLine, str ):
                    print( 'Calling by passing subprocess func args obj: ', argsForCommandLine )
                else:
                    print( 'Calling: ', argsForCommandLine )
                
                print( '-------- Start of Call --------' )
        
        if interactive==True:
            r = subprocess.run(
                argsForCommandLine,
                shell=True
            )   
        else:
            r = subprocess.run(
                argsForCommandLine,
                shell=True,
                universal_newlines=True,  #text=True  only since py3.8
                #capture_output=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
        
        if not quiet:
            print( (r.stdout) )
            if loud==True:
                print( '-------- End Of Call --------' )
                
        return r
        
    @classmethod
    def CallInteractive( cls, *args, **kwargs ):
        kwargs['interactive']=True
        try:
            cls.CallActual( *args, **kwargs )
        except KeyboardInterrupt:
            print( "Interrupted by keyboard (ctrl-c probably) when running:", *args )

    @classproperty
    def CallI( cls ):
        return cls.CallInteractive
    
    @classmethod
    def CallLoud( cls, *args, **kwargs ):
        kwargs['loud']=True
        return cls.CallActual( *args, **kwargs )

    @classproperty
    def CallQ( cls ):
        return cls.CallQuiet
       
    @classmethod
    def CallQuiet( cls, *args, **kwargs ):
        kwargs['quiet']=True
        return cls.CallActual( *args, **kwargs )

    @classproperty
    def CbCopy(cls):
        return cls.PyperclipCopy
    
    @classproperty
    def CbPaste(cls):
        return cls.PyperclipPaste

    @classproperty
    def Cd0(cls):
        return cls.CdToScriptDir
        
    @classmethod
    def CdToScriptDir(cls):
        cls.Mods.os.chdir( cls.ScriptDir )

    
    @classproperty
    def Cd(cls):
        return Funcs.Cd
    
    #@classproperty
    #def CheckForXonsh(self):
    #    return Utils.CaseInsensitiveDict
    
    #@classproperty
    #def checkForXonsh(self):
    #    return Utils.CaseInsensitiveDict
    
    @classproperty
    def CiDict(cls):
        return Utils.CaseInsensitiveDict
    
    @classproperty
    def CaseInsensitiveDict(cls):
        return Utils.CaseInsensitiveDict

    @classproperty
    def ClassProperty(cls):
        return Utils.Funcs.classproperty
    @classproperty
    def ClassMethod(cls):
        return classmethod
         
    @classproperty
    def Code(cls): ## property can't pass *args, **kwargs
        #print( 'Code is being processed and run by joeccbatpy... ' + cls.Inst.argv0 + '' )
        return cls.CodeQuiet
        
    @classproperty
    def CodeQ(cls):  ## property can't pass *args, **kwargs
        return cls.CodeQuiet
        
    @classproperty
    def CodeQuiet(cls):  ## property can't pass *args, **kwargs
        return cls.Inst.getCode()

    @classproperty
    def ContextManager(cls):
        return Funcs.ContextManager


    @classproperty
    def CurrentWorkDir( cls ):
        return cls.GetCwd()
 
    @classproperty
    def Cwd( cls ):
        return Funcs.GetCwd()
       
    @classproperty
    def Dataclass( cls ):
        return Easy.Mods.dataclasses.dataclass
       
    @classproperty
    def DataClass( cls ):
        return Easy.Mods.dataclasses.dataclass
    
    @classproperty
    def Dataclasses( cls ):
        return Easy.Mods.dataclasses
   
    @classproperty
    def DataClasses( cls ):
        return Easy.Mods.dataclasses
   
    @classproperty
    def DictOfDefaultsOntoObj( cls ):
        return Funcs.DictOfDefaultsOntoObj
    
    @classproperty
    def DictOfDefaultsOntoDict(cls):
        return Funcs.DictOfDefaultsOntoDict
    
    ## *** todo
    def Dir(cls):
        'pass'
        
    @classproperty
    def DirsyncFunc(cls):
        """
        Usage Example:
        
        Easy.DirsyncFunc( src, dest, actionStr, optionsDict ) 
        
        
        to use actions/options in function call, do not include "--"
        use  'sync'  not '--sync'

        for dict values True and False should work
        or strings or lists of string for things like excludes 
        
        
        See https://github.com/tkhyn/dirsync/ for full options
        
        
        Main Options
        
        --diff, -d     Only report difference between sourcedir and targetdir
        --sync, -s     Synchronize content between sourcedir and targetdir
        --update, -u     Update existing content between sourcedir and targetdir
        
        If you use one of the above options (e.g. sync) most of the time, you may consider defining the action option in a Configuration file parsed by dirsync.
        Additional Options
        --verbose, -v     Provide verbose output
        --purge, -p     Purge files when synchronizing (does not purge by default)
        --force, -f     Force copying of files, by trying to change file permissions
        --twoway, -2     Update files in source directory from target directory (only updates target from source by default)
        --create, -c     Create target directory if it does not exist (By default, target directory should exist.)
        --ctime     Also takes into account the source file's creation time (Windows) or the source file's last metadata change (Unix)
        --content     Takes into account ONLY content of files. Synchronize ONLY different files. At two-way synchronization source files content have priority if destination and source are existed
        --ignore, -x patterns
             Regex patterns to ignore
        --only, -o patterns
             Regex patterns to include (exclude every other)
        --exclude, -e patterns
             Regex patterns to exclude
        --include, -i patterns
             Regex patterns to include (with precedence over excludes)
        """
        from .submodules.dirsync import sync
        return sync
        
    def DirToObj(cls):
        'pass'

        
    @classproperty
    def Easy(cls):
        return cls.Magic
        
    @classproperty
    def EasyConf(cls):
        return EasyConf
    @classproperty
    def EasyMod(cls):
        return cls.SelfMod
    
    @classproperty
    def EnumArgs(cls):
        return Funcs.EnumArgs
    
    @classproperty
    def EnvGet(cls):
        return Funcs.EnvGet
    
    @classproperty
    def Env(cls):
        return Easy.Mods.os.environ
        
    @classproperty
    def Envs(cls):
        return Easy.Mods.os.environ




    @classmethod
    def EscArgForWin(cls, arg):
        """
        see notes in EscArgsForCmdExe
        """
        import re
        reObj = re.search(r'(["\s])', arg)
        if not arg or reObj:
            arg = '"' + arg.replace('"', r'\"') + '"'
        return arg
        
    @classmethod
    def EscArgsForWin( cls, args, join=True ):
        """
        see notes in EscArgsForCmdExe
        """
        if isinstance( args, str ):
            raise "EscArgsForWin needs a nonstring like iterable container, such as a list"
        escArgs = []
        for arg in args:
            esc = cls.EscArgForWin( arg )
            escArgs.append( esc )
        if join==True:
            escArgs = ' '.join( escArgs )            
        return escArgs

    @classmethod
    def EscArgForCmdExe(cls, arg, alsoEscapeForWin=True):
        """
        arg should already be escaped for CommandLineToArgvW
        or whatever other parsing engine the eventual  program using the arg expects
        
        see notes in escArgsForCmdExe func
        """
        if alsoEscapeForWin:
            arg = cls.EscArgForWin( arg )
        import re

        def escapeCharsToEsc(m):
            char = m.group(1)
            return charsMap[char]

        charsToEsc = '()%!^"<>&|'
        reObj = re.compile('(' + '|'.join(re.escape(char) for char in list(charsToEsc)) + ')')
        charsMap = { char: "^%s" % char for char in charsToEsc }
        escaped = reObj.sub(escapeCharsToEsc, arg)
        return escaped

    @classmethod
    def EscArgsForCmdExe(cls, args, alsoEscapeForWin=True, join=True):
        """
        do not use this one normally, only for complex things
        with |%>< etc literals
        where you don't want the arg to cause redirects/pipes/etc
        normally if running a shell command you probably do want
        redirects etc unless cmd or args are from an untrusted source
        in which case this Easy system shouldn't be used.
        
        windows and cmd.exe may need two layers of escaping
        once for CommandLineToArgvW and once for cmd.exe
        
        see: https://stackoverflow.com/questions/29213106/how-to-securely-escape-command-line-arguments-for-the-cmd-exe-shell-on-windows#29215357

        ## and See http://blogs.msdn.com/b/twistylittlepassagesallalike/archive/2011/04/23/everyone-quotes-arguments-the-wrong-way.aspx
        """
        if isinstance( args, str ):
            raise "EscArgsForWin needs a nonstring like iterable container, such as a list"
        escArgs = []
        for arg in args:
            esc = cls.EscArgForCmdExe( arg, alsoEscapeForWin=alsoEscapeForWin )
            escArgs.append( esc )
        if join==True:
            escArgs = ' '.join( escArgs )
        return escArgs
        
    def EscArgForPosix(cls, arg):
        import shlex
        return shlex.quote( arg )
        
    def EscArgsForPosix(cls, args):
        import shlex
        escArgs = []
        for arg in args:
            esc = shlex.quote(arg)
            escArgs.append(arg)
        return escArgs
        
    def EscArgs( cls, args ):
        """
        this function should check for platform and potentially cmd.exe / shell
        to determine how to escape the arguments, then
        Call functions can automatically incorporate it as well
        """
        raise "not implemented"
    
        
    @classproperty
    def Eval(cls):
        return Funcs.Eval

    @classproperty
    def ExtendBuiltinClass(cls):
        return Funcs.ExtendBuiltinClass

    @classproperty
    def Exit(cls):
        return Funcs.Exit
        
    @classmethod
    def FileRead(cls, filePath ):
        fh = open( filePath )
        contents=txt = fh.read()
        fh.close()
        return contents
        
        
    @classproperty
    def Flib(cls):
        return cls.Inst.flib
        
    @classproperty
    def Fstring( cls ):
        return Funcs.Fstring
    @classproperty
    def Format(cls):
        return Funcs.Format
    @classproperty
    def FormatV( cls):
        return Funcs.FormatV
    @classproperty
    def Frame(cls):
        return Funcs.Frame
    @classmethod
    def FromFrame(cls):
        return Funcs.FromFrame
        
    @classproperty
    def Funcs(cls):
        return Funcs

    @classproperty
    def GetCwd( cls ):
        # i = cls.Inst
        return Funcs.GetCwd
    
    @classproperty
    def Getcwd( cls ):  ## just an alternative capitalization
        return Funcs.GetCwd
        
    @classproperty
    def GetFirstNonNoneElseReturnNone(cls):
        return Funcs.GetFirstNonNoneElseReturnNone
    
    @classproperty
    def GetRoutinesFromObj(cls):
        return Funcs.GetRoutinesFromObj

    @classproperty
    def Glob(cls):
        return Funcs.Glob    

    @classproperty
    def Global(cls):
        if cls.__Global == None:
            cls.__Global = Object()
        return cls.__Global
        

    @classproperty
    def Ic(cls):
        return Funcs.Ic
        
    @classproperty
    def Import(cls):
        return Funcs.Import
           
    @classproperty
    def ImportFile( cls ):
        return Funcs.ImportFile
    
    
    @classmethod
    def IncrementReloadCount(cls): 
        cls.__ReloadCount += 1
        return cls
    
    @classmethod
    def Init0(cls):
        """
        Init singleton instance of class without
        auto chir or auto load code.
        """
        cls.Init(
            shouldAutoChdirToArg0Dir=False, shouldAutoLoadCode=True
        )
        return cls.__SingletonInstance
    
    @classmethod
    def Init(cls, 
            shouldAutoChdirToArg0Dir=True,
            shouldAutoLoadCode=True,):
        """
        Auto Initializes the Easy module with default Easy Options
        Does things like change working dir.
        """
        if cls.__SingletonInstance==None:
            cls.__SingletonInstance = cls(
                shouldAutoInit=True,
                shouldAutoChdirToArg0Dir=shouldAutoChdirToArg0Dir,
                shouldAutoLoadCode=shouldAutoLoadCode,
            )
        else:
            cls.__SingletonInstance.init()
            
        return cls.__SingletonInstance
    
    @classmethod
    def Input( cls, *args, **kwargs):
        return cls.Keys.Input(*args, **kwargs)
        ## used to have more opts, 
        ## prompt, timeout=None, default=None, warn=True 
             
    @classproperty
    def Inst(cls):
        if cls.__SingletonInstance==None:
            cls.__SingletonInstance = cls()
        return cls.__SingletonInstance
    
    @Inst.setter
    def InstSetter( cls ):
        #print( 'no setter available' )
        raise AttributeError("Can't assign to readonly Inst property")

    @classproperty
    def Ipy(cls):
        from . import Ipy
        return Ipy.EasyIpy



    @classproperty
    def JoinDir(cls):
        return Funcs.JoinDir
    
    @classproperty
    def JoinDirs(cls):
        return Funcs.JoinDir
    
    @classproperty
    def JoinDirFileExt(cls):
        return Funcs.JoinDirFileExt 
            
    """
    @classproperty
    def KeypressList(cls):
        return cls.EasyKeys.KeypressList
    @classproperty
    def KeypressStr(cls):
        return cls.Keys.KeypressStr
    @classproperty
    def KeyUtils(cls):
        return cls.KeysMod.EasyKeysClsFuncs
    @classproperty
    def KeyInput(cls):
        return cls.EasyKeys.Input
    """
    
    @classproperty
    def Keys(cls):
        ## change this later to use real ones,
        ## not Utiks  
        return cls.KeysMod.EasyKeys
    
    @classproperty
    def KeysMod(cls):
        from . \
            import EasyKeys \
                as EasyKeysMod
        return EasyKeysMod


    @classmethod  ## for some reason, as @classproperty caused problems w *args, **kwargs
    def Log(cls,*args, **kwargs):
        from . import Logger     
        return Logger.Logger.Log(*args,**kwargs)

    @classproperty
    def Logger(cls): 
        from . import Logger       
        return Logger.Logger
    
    @classproperty
    def Logging(cls):
        import logging
        return logging
    
    @classmethod ## for some reason, as @classproperty caused problems w *args, **kwargs
    def Llog(cls, *args, **kwargs): 
        from . import Logger     
        return Logger.Logger.Llog(*args,**kwargs)
    
    
    @classproperty
    def LogFormatDisable(cls, format='' ):
        from . import Logger       
        return Logger.Logger.LogFormatDisable
            
    @classproperty
    def LogFormatEnable(cls, format=None ):
        from . import Logger       
        return Logger.Logger.LogFormatEnable
            
    @classproperty
    def LogFormatCtx(cls, format='' ):
        from . import Logger       
        return Logger.Logger.LogFormatCtx
    
    @classmethod ## for some reason, as @classproperty caused problems w *args, **kwargs
    def LogN(cls, *args, **kwargs ):
        from . import Logger       
        return Logger.Logger.LogN(*args, **kwargs)
    
    @classmethod ## for some reason, as @classproperty caused problems w *args, **kwargs
    def LlogN(cls, *args, **kwargs ):
        from . import Logger       
        return Logger.Logger.LlogN(*args, **kwargs)

    @classproperty
    def LogSetLevel(cls, level):
        from . import Logger       
        return Logger.Logger.LogSetLevel   
        
    @classproperty
    def LogGetDefaultLogger(cls):
        from . import Logger       
        return Logger.Logger.GetDefaultLogger
        
    
        
    
    """
    @classmethod
    def Logger(cls, default=info, ):
        import logging
        n = cls.Namespace()
        ## these are simplified levels,
        ## not the real ints since error int is actually 40 etc
        simpleIntsToLevels = {
            0:'debug',
            1:'debug',
            2:'info',
            3:'warning',
            4:'error',
            5:'critical',
        }
        simpleLevelsToInts = {}
        for k,v in intsToLevels.items():
            levelsToInts[v]=k
            
        if isinstance( level, int):
            level = simpleIntsToLevels[]
            
        ##
        intsToLevels = {
            50='critical'
            40='error'
            30='warning'
            20='info'
            10='debug'
            0='notset'
        }
        assert logging.CRITICAL=50
        assert logging.ERROR=40
        assert logging.WARNING=30
        assert logging.INFO=20
        assert logging.DEBUG=10
        assert logging.NOTSET=0
        
        n.simpleIntsToLevels = simpleIntsToLevels
        n.simpleLevelsToInts = simpleLevelsToInts
        n.l1=logging.debug
        n.l2=logging.debug
        n.l3=logging.warning
        n.l3=logging.error
        n.l3=logging.critical
        n.l0=[l1,l2,l3,l4,l5] ## this one is zero based index
        n.l=[ l1,l1,l2,l3,l4,l5 ] ## this one has indexes that match levels
        
        n.log = cls.Log
        return n  ## return the new loger object
    
    #@def
    """
        

    @classproperty
    def Ls(cls):
        return Funcs.Ls
    
    @classproperty
    def LsAbs(cls):
        return Funcs.LsAbs
    
    ## We call it "Magic" because it triggers all kinds of background
    ## stuff to happen.  Magic often implies that
    ## in common coder terminologys
    @classproperty   
    def Magic(cls):
        cls.Init()
        return cls.Inst.getCode()

    @classproperty
    def MagicConf(cls):
        return EasyConf.MagicConf

    @classproperty
    def Mod(cls):
        return SelfMod
    
    @classproperty
    def Mods(cls):
        return cls.Inst.modules

    @classproperty
    def Module(cls):
        return __import__( __name__ )
        
    
    @classproperty
    def Modules(cls):
        return cls.Inst.modules    
    
    @classproperty
    def ModFromName(cls,name):
        import sys
        return sys.modules(name)
    
    @classproperty
    def NamedTuple(cls):
        return Easy.Mods.collections.namedtuple    

    @classmethod
    def Namespace(cls):
        return Funcs.Namespace
        
    @classmethod
    def NamespaceComplex(cls):
        return Funcs.NamespaceComplex   
    
    @classproperty
    def Now(cls):
        return Funcs.Now
    @classproperty
    def NowUtc(cls):
        return Funcs.NowUtc
    @classproperty
    def NowAsUtc(cls):
        return Funcs.NowUtc
    @classproperty
    def NowAsLocal(cls):
        return Funcs.NowLocal
    @classproperty
    def NowLocal(cls):
        return Funcs.NowLocal
    @classproperty
    def NowLocalStr(cls):
        return Funcs.NowLocalStr

    @classproperty
    def ODict(cls, *args,**kwargs):
            ## *args, and **kwargs are defensive
            ##  might not be needed for this to work
        return Funcs.ODict

    @classproperty
    def OrderedDict(cls, *args,**kwargs):
            ## *args, and **kwargs are defensive
            ##  might not be needed for this to work
        return Funcs.ODict

    @classproperty
    def OrigWorkDir( cls ):
        return cls.Inst.origWorkDir
   
        
    #@classmethod
    #def Pip( cls, *args, action='install', installMode='user', **kwargs ):
    #    print( 'Easy.Pip not yet implemented')
    #    #if action=='install'
    
    @classproperty
    def PipInstall( cls ):
        return Funcs.PipInstall
    @classproperty
    def Pprint(cls):
        return Easy.Mods.pprint.pprint
    
    @classproperty
    def PPrint(cls):
        return Easy.Mods.pprint.pprint
    
    @classproperty
    def Prints(cls):
        return Funcs.Prints
    @classproperty
    def PrintFile(cls):
        return Funcs.PrintFile
    @classproperty
    def PrintLoop(cls):
        return Funcs.PrintLoop
    @classproperty
    def PrintTail( cls ):
        return Funcs.PrintTail
        
    @classproperty
    def PrintTraceback(cls):
        return Funcs.PrintTraceback
    @classproperty
    def PrintTb(cls):
        return Funcs.PrintTraceback
    @classproperty
    def Ptb(cls):
        return Funcs.PrintTraceback
        
    @classproperty
    def PrintVar(cls):
        return Funcs.PrintVar
        
    @classproperty
    def PrintVars(cls):
        return Funcs.PrintVars
        
    @classproperty
    def PrintWithFormat( cls ):
        return Funcs.PrintWithFormat
    
    @classproperty
    def PrintWithFormatV( cls ):
        return Funcs.PrintWithFormatV
    
    @classproperty
    def PyperclipMod(cls):
        from .submodules import pyperclip
        return pyperclip
    @classproperty
    def Pyperclip(cls):
        return cls.PyperclipMod
    @classmethod
    def PyperclipCopy(cls, text):
        return cls.PyperclipMod.copy(text)
    @classmethod
    def PyperclipPaste(cls):
        return cls.PyperclipMod.paste()
    
    @classmethod
    def PyperclipDetermineClipboard( cls ):
        return cls.PyperclipMod.determine_clipboard( )
    @classmethod
    def PyperclipSetClipboard(cls, clipboardMechanism ):
        """
        explicitly set clipboard backend 
        pbcopy,pbobjc (default on Mac OS X),gtk,qt,xclip,xsel,klipper,windows (default on Windows)
        """
        return cls.PyperclipMod.set_clipboard(clipboardMechanism)
    @classmethod
    def PyperclipWaitForPaste(cls, timeout=None):
        return cls.PyperclipMod.waitForPaste(timeout=None)
    @classmethod
    def PyperclipWaitForNewPaste(cls, timeout=None):
        return cls.PyperclipMod.WaitForNewPaste(timeout=timeout)
    @classproperty
    def PyperclipException(cls):
        from . import pyperclip
        return cls.PyperclipMod.PyperclipException
    @classproperty
    def PyperclipWindowsException(cls):
        from . import pyperclip        
        return cls.PyperclipMod.PyperclipWindowsException
    @classproperty
    def PyperclipTimeoutException(cls):
        return cls.PyperclipMod.PyperclipTimeoutException
                              
    @staticmethod
    def ReloadModule( targetMod=None, name=None):
        return Funcs.ReloadModule(
            targetMod=targetMod, name=name,
            fallbackMod=SelfMod,
        )
            
    @classproperty
    def ReloadStr( cls ):
        return cls.__ReloadStr
    
    @classmethod
    def Reload( cls, quiet=False ):
        import importlib
        if not quiet:
            print( EasyConf.ReloadWarning )
        try:
            count = cls.__ReloadCount
            if cls.__SingletonInstance!=None:
                cls.__SingletonInstance.deleteTmpFile()
            mod = importlib.reload(  __import__( __name__ )  )
            count += 1
            mod.Easy._SetReloadCount( count )
            print( f"Reload of Easy module complete. " 
                   f"Reload count is now: {count}"
            )
            return mod.Easy
        except Exception as e:
            if not quiet:
                cls.PrintTraceback()
                print( "Reload of Easy module failed." )
                return SelfMod.Easy
            raise( e )
        
    
    
    @classproperty
    def ReloadCount(cls): 
        return cls.__ReloadCount

    @classmethod
    def ReverseEnumList( ls ):
        for i in range( len(ls) - 1, -1, -1):
            yield i, ls[i]
            
    @classmethod
    def ReverseRangeList( ls ):
        for i in range( len(ls) - 1, -1, -1):
            yield i
            

    
    @classproperty
    def Rreplace(cls):
        return Funcs.Rreplace
    
    @classproperty
    def ReplaceEnd(cls):
        return Funcs.ReplaceEnd

    @classproperty
    def ScriptDir( cls ):
        return cls.Inst.argv0Dir
    
    @classproperty
    def See(cls):
        return Funcs.See
        
        
    
    @classproperty
    def SelfMod( cls ):
        return SelfMod
    
    @classproperty
    def SelfPackage( cls ):
        return SelfPak
    @classproperty
    def SelfPak( cls ):
        return SelfPak
    
    @classproperty
    def Sleep(cls):
        return Funcs.Sleep
    
    @classmethod
    def SplitExt(cls, path,):
        import os
        return os.path.splitext( path )
    
    @classmethod
    def SplitDirFileExt(cls, path,): #cleanTrailingSlashes=False):
        import os
        sep = os.path.sep

        dr, filename = os.path.split(path)
        if len(filename)==0:
            filebasename=''
            ext=''
        else:
            filebasename, ext = os.path.splitext( filename )
            
        return dr, filebasename, ext
    
        
    @classmethod
    def StrFixMl(cls, orig):
        """
        If there is only whitespace after the last newline
        remove the last newline and all whitespace after it
        """
        fixed = orig
        if len(fixed)>0:
            lines = fixed.splitlines()
            #assert( len )
            ## if there's more than one line
            ## remove first line if it's empty whitespace
            if len(lines)>1:
                if lines[0].lstrip()=='':
                    del lines[0]
            ## if there's more than one line left
            ## remove empty whitespace line at end
            if len(lines)>1:
                if lines[-1].rstrip()=='':
                    del lines[-1]
            fixed = "\n".join( lines )
        """
            ## remove leading newline
            if fixed.startswith('\n'):
                fixed = fixed[1:]
            if '\n' in fixed:
                frags = fixed.rsplit('\n',1)
                frags[-1] = frags[-1].rstrip()
                ## if the last grag is empty now, remove it
                if frags[-1]=='':
                    frags = frags[:-1]
                fixed = "\n".join(frags)
        """
        return fixed
            
    @classmethod
    def StrReplaceStart( cls, st, pat, repl ):
        if len(pat)==0:
            return st
        elif not st.startswith( pat ):
            return st
        elif len(pat) > len(st):
            return st
        else:
            return repl + st[len(pat):]  ## st.replace( pat, repl, 1 )
        
    @classmethod        
    def StrReplaceEnd( cls, st, pat, repl, ):
        if len(pat)==0:
            return st
        elif not st.endswith(pat):
            return st
        elif len(pat) > len(st):
            return st
        else:
            return st[:-len(pat)] + repl


    
    @classmethod
    def SubInteract( cls, *args, capture_output=False, **kwargs ):
        import subprocess
        sub = subprocess.run( *args, capture_output=capture_output, **kwargs )
        return sub
 
    """
    Should change the SysXX cmds below to use platform.system instead
    gives values like  Windows   Linux  Darwin  etc
      os.name or sys.platform are other ones, might be less useful
              sys.platform get sys it was *BUILT ON*  not useful
    Easy.Mods.platform.system()
    
    """
    
    @classproperty
    def Sys(cls):
        import sys
        return sys
        
    #@classproperty
    #def SysModules(cls):
    #    import sys
    #    return sys.modules


    @classproperty
    def SysIsLinuxLike(cls):
        """
        Liknux like means any non-mac non-windows
        system that's mostly posix.
        """
        import os
        import platform
        if (os.name=='posix' and
              (not platform.system().lower().startswith('darwin') )
            ):
            return True
        else:
            return False
    
    
    @classproperty
    def SysIsMac(cls):
        """
        Windows means MacOS or Mac OSX etc
          modern macs circa 2022
            also known as "Darwin"
        """        
        import sys
        return sys.platform.lower().startswith('darwin')
    
    @classproperty
    def SysIsOther(cls):
        """
        Windows means MacOS or Mac OSX etc
          modern macs circa 2022
            also known as "Darwin"
        """        
        import sys
        return not (
            cls.SysIsMac or cls.SysIsWindows
            or cls.SysIsLinuxLike
        )
    
    @classproperty
    def SysIsWindows(cls):
        """
        Windows means modern windows circa 2022
          decended/derived from nt
            nt>2000>XP>Vista>7>8>10>11>etc
            support the win32 api etc
        """
        import os
        return os.name=='nt'


        
    @classmethod
    def Tail( cls, *args, **kwargs ):
        argsList = list(args) ##
        n = kwargs.pop( 'n', 5 )
        tailsep = kwargs.pop( 'tailsep', '\n\n' )
        asList=kwargs.pop( 'asList', False )
        
        nl='\n'
                
        tails = []
        for arg in argsList:
            r = nl.join(  arg.split( nl )[ -1-n : None ] )
            tails.append( r )
            
        if asList:    
            return tails
        else:
            s = tailsep.join( tails )
            return s


    @classmethod
    def TimeoutDefault( cls, timeout, default, func, *args, **kwargs ):
        result = cls.TimeoutFull( timeout, func, *args, **kwargs )
        if isinstance( result, EasyReturnedTimeout ):
            return default
        else:
            return result  

    @classproperty
    def Tb(cls):
        return Funcs.Traceback    
    
    @classmethod
    def TimeoutErr( cls, timeout, func, *args, **kwargs ):
        result = cls.TimeoutFull( timeout, func, *args, **kwargs )
        if isinstance( result, EasyReturnedTimeout ):
            raise result
        else:
            return result
    
    @classmethod
    def Timeout( cls, timeout, func, *args, **kwargs ):
        """
        note, won't call cleanup, e.g.
        won't even give newline after canceled input
        only use for really simple things that are very safe to kill
        
        """
        #opts can simply be a number for the timeout time length
        #  but is extensible in future by being a dict like
        #  
        #note this func works badly with keyboard input
        #try:
        #  timeout = float(opts)
        #except:
        #  timeout=opts['timeout']
        
        result = cls.TimeoutFull( timeout, func, *args, **kwargs )
        if isinstance( result, EasyReturnedTimeout ):
            result = None
        return result
    
    @classmethod
    def TimeoutFull( cls, timeout, func, *args, **kwargs ):
        
        t = EasyThread(
            group=None,  name=None,
            target=func,
            args=args,
            kwargs=kwargs
        )
        t.setDaemon(True) ## make it not keep main thread alive
        t.start()
        response = t.join(timeout=timeout)
        t.kill()
        return response
                

    @classproperty
    def TmpDir( cls ):
        return Funcs.TmpDir
        
    @classproperty  ## *** todo  make this a property
    def Traceback(cls):
        return Funcs.Traceback

    @classproperty
    def TrimAndTab( cls):
        return Funcs.TrimAndTab
    @classproperty
    def Tt( cls):
        return Funcs.TrimAndTab
    
    @classproperty
    def TrimLines( cls ):
        return Funcs.TrimLines
    @classproperty
    def Tl( cls ):
        return Funcs.TrimLines

    """
    @classmethod
    def TrimTodo( cls, st ):
        return st
    """    
        
    @classproperty
    def TzOff(cls):
        return Funcs.TzLocal
        
    @classproperty
    def TzLocal(cls):
        return Funcs.TzLocal

    @classmethod
    def Uuid(cls, *args, **kwargs):
        return cls.Uuid1( *args, **kwargs)

    @classmethod
    def UuidRand(cls, *args, **kwargs):
        return cls.Uuid4( *args, **kwargs)

    
    @classmethod
    def Uuid1(cls, *args, **kwargs):
        import uuid
        return uuid.uuid1( *args, *kwargs )
 
    @classmethod
    def Uuid1(cls, *args, **kwargs):
        import uuid
        return uuid.uuid1( *args, *kwargs )
 
    @classmethod
    def Uuid3(cls, *args, **kwargs):
        import uuid
        return uuid.uuid3( *args, *kwargs )
 
    @classmethod
    def Uuid4(cls, *args, **kwargs):
        import uuid
        return uuid.uuid5( *args, *kwargs )
 
    @classmethod
    def Uuid5(cls, *args, **kwargs):
        import uuid
        return uuid.uuid5( *args, *kwargs )
 
    @classproperty
    def UniqueIntHuge(cls):
        return Funcs.UniqueIntHuge
           
    @classproperty
    def Utils(cls):
        return Utils

    @classproperty
    def VirtualEnvCheck(cls):
        sys = Easy.Mods.sys
        """Get base/real prefix, or sys.prefix if there is none."""
        basePrefix = getattr(sys, "base_prefix", None)
        realPrefix = getattr(sys, "real_prefix", None) or sys.prefix
        prefix = basePrefix or realPrefix
        ## if in virtualenv sys.prefix will be different than prefix
        return prefix != sys.prefix
    
    @classmethod
    def Walk(cls, pth):
        from . import Walker
        for i in Walker.Walker.walk(pth):
            yield i
    @classmethod
    def WalkAnIter(cls, paths):
        from . import Walker
        for i in Walker.Walker.WalkAnIter(paths):
            yield i
    @classproperty
    def Walker(cls):
        from . import Walker
        return Walker
    @classproperty
    def Wwalk(cls):
        return cls.Walk
    
    
    @classmethod
    def Win32GetProcessPriorityById(cls, pid):
        import subprocess
        cmd = 'wmic process where "ProcessId=' +str(pid) + '" get priority'
        r =  subprocess.check_output( cmd, shell=True )
        rl = r.splitlines()
        '''
        for i,v in enumerate(rl):
            print( f" i: {i}  v: {v} " )
            """
             i: 0  v: b'Priority  '
             i: 1  v: b''
             i: 2  v: b'4         '
             i: 3  v: b''
             i: 4  v: b''
             i: 5  v: b''
            """
        '''
        return int( rl[2].strip() )
        #wmic process get name,priority 


    @classmethod
    def Win32SetProcessPriorityToLowest(cls, pid):
        """
        idle: 64 (or "idle")
        below normal: 16384 (or "below normal")
        normal: 32 (or "normal")
        above normal: 32768 (or "above normal")
        high priority: 128 (or "high priority")
        real time: 256 (or "realtime")
        
        this doesn't map directly to internal numbers unfortunately
        e.g. getpriority 8 is normal
        should remap it myself
        """
        """ Set the priority of the process to below-normal."""
        cmd = "wmic process where processid=\""+str(pid)+"\" CALL   setpriority \"idle\""
        #print( cmd )
        import subprocess, os, sys
        subprocess.check_output( cmd, shell=True)

    @classmethod
    def Win32GetProcessIdListByName(cls, name):
        """
        returned objects have properties including the following:
        class Win32_Process : CIM_Process
        {
          string   CreationClassName;
          string   Caption;
          string   CommandLine;
          datetime CreationDate;
          string   CSCreationClassName;
          string   CSName;
          string   Description;
          string   ExecutablePath;
          uint16   ExecutionState;
          string   Handle;
          uint32   HandleCount;
          datetime InstallDate;
          uint64   KernelModeTime;
          uint32   MaximumWorkingSetSize;
          uint32   MinimumWorkingSetSize;
          string   Name;
          string   OSCreationClassName;
          string   OSName;
          uint64   OtherOperationCount;
          uint64   OtherTransferCount;
          uint32   PageFaults;
          uint32   PageFileUsage;
          uint32   ParentProcessId;
          uint32   PeakPageFileUsage;
          uint64   PeakVirtualSize;
          uint32   PeakWorkingSetSize;
          uint32   Priority = NULL;
          uint64   PrivatePageCount;
          uint32   ProcessId;
          uint32   QuotaNonPagedPoolUsage;
          uint32   QuotaPagedPoolUsage;
          uint32   QuotaPeakNonPagedPoolUsage;
          uint32   QuotaPeakPagedPoolUsage;
          uint64   ReadOperationCount;
          uint64   ReadTransferCount;
          uint32   SessionId;
          string   Status;
          datetime TerminationDate;
          uint32   ThreadCount;
          uint64   UserModeTime;
          uint64   VirtualSize;
          string   WindowsVersion;
          uint64   WorkingSetSize;
          uint64   WriteOperationCount;
          uint64   WriteTransferCount;
        };        
        """
        procLs = cls.Win32GetProcessNameListByName( name )
        ids = []
        for proc in procLs:
            ids.append( int(proc.ProcessId) )
        return ids
        
    @classmethod
    def Win32GetProcessNameListByName(cls, name):
        wmiProcs = []
        import wmi
        c = wmi.WMI ()
        psList = c.Win32_Process ()
        for iProc in psList:
            if iProc.Name==name:  ##.startswith( "WmiPrvSE"):
                wmiProcs.append( iProc )
        return wmiProcs

    @classmethod
    def Xi(cls, cmd, *args, **kwargs ):
        """
            Run an interactive subprocess command
            mostly for running bash commands
        
            On LinuxLike (incl BSD) and Mac Systems
            will always use bash to run it
            via:  "/bin/bash -i -c "
            
            Doesn't work with mc in ipython, not sure why
        """
        if cls.SysIsWindows:
            print( 'is windows' )
            return cls.SubInteract( cmd, shell=True )
        elif cls.SysIsLinuxLike or cls.SysIsMac:
            shellExe='/bin/bash'
            return cls.SubInteract( [ shellExe, '-i', '-c', cmd ]  )
        else:
            raise NotImplementedError

    @classmethod           
    def Ytdl(cls, *args, **kwargs ):
        return cls.YtdlMod.ytdl( *args, **kwargs )
        
    @classproperty           
    def YtdlIter(cls):
        return cls.YtdlMod.ytdlIter
                
    @classproperty          
    def YtdlMod(cls):
        from . import Ytdl as YtdlMod
        return YtdlMod
        
    
    
    
    ##################################
    #### Instance Methods and Properties
    
    def __init__(self,*args,
            shouldAutoInit=False,
            shouldAutoChdirToArg0Dir=False,
            shouldAutoLoadCode=False,
            shouldAutoRecode='unimplemented'
        ):
        """
        args can be used to override
            shouldAutoInit=False,
            shouldAutoChdirToArg0Dir=False,
            shouldAutoLoadCode=False,
            easyInst = Easy(1,0,0)
              ## will auto init but not chdir or load code 
        """
        import os, sys
        ## allow some quick overrides of longer options
        if len(args):
            shouldAutoInit=bool(args[0])
            if len(args)>1:
                shouldAutoChdirToArg0Dir=bool(args[1])
                if len(args)>2:
                    shouldAutoLoadCode=bool(args[2])  
        
        self.__shouldAutoInit = shouldAutoInit
        self.__shouldAutoChdirToArg0Dir = shouldAutoChdirToArg0Dir
        self.__shouldAutoLoadCode = shouldAutoLoadCode
         
        ## set vars, direct/simple
        self.cls = self.__class__
        self.recodeRequiresMagicExit = True
        self.code = None
        self.codeLoaded = None
        self._hasBeenRecoded=False
        self._hasBeenInit=False
        
        
        ## set vars, computed and classes
        self.origWorkDir = os.getcwd()
        self.modules = ModulesLazyLoader.ModulesLazyLoader()
        
        self.functionLibrary = Utils.FunctionLibrary()

        ## Get a copy of original sys.argv at time of program start
        self.argvOrig = sys.argv.copy()
        ## Get a copy of argv to change in case we have to
        self.argv = sys.argv.copy()  
        
        ## check and assert that we have a properly formed argv
        assert len(self.argv)>0 ## should at least have the executed script
        assert type(sys.argv[0])==str  ## it should be a string        
        ## now that it's verified, we get it
        self.argv0 = self.argv[0]

            
        ## try to get real paths for sys.argv0
        try:
            assert type( self.argv0 ) == str
            if self.argv0 != "":
                self.argv0 = os.path.realpath( self.argv0 )
        except:
            self.argv0=''
        self.argv0Dir = os.path.dirname( self.argv0 )
        ## we'll try again after full init
        

        ## Have tmp vars originally set to None
        ## if they are still none later, it means we didn't use them
        self.tmpFile = None        ## will be file handle if needed
        self.tmpFileName = None   ## will be file name if needed
        
        if self.__shouldAutoInit:
            self.init()
        
    
    def init(self):  ## intentionally takes no arguments other than self
        global os
        import os
        if self._hasBeenInit==True:
            return self
        ## Fallback via temporary argv fake file
        ## In case argv0 isn't a real script, fake a temporary one
        if self.argv0=="":
            self.atInitFallbackInCaseNoArg0()
            
        ## Make sure our argv0 is a real abs path
        self.argv0 = os.path.realpath( self.argv0 )
        self.argv0Dir = os.path.dirname( self.argv0 )
        
        ## Get code from arg0 file
        if self.__shouldAutoLoadCode:
            self.loadCode()
            
        if self.__shouldAutoChdirToArg0Dir:
            self.chdirOnInit()
            
        return self
        
    def actionCall(self, *args, **kwargs ):
        self.CallActual( *args, **kwargs )

    def atInitFallbackInCaseNoArg0(self):
        tmpFile = tempfile.NamedTemporaryFile(
            mode='r', suffix='.jocceasy.tmp.py', delete=False,
        )
        tmpFileName = os.path.realpath( tmpFile.name )
        atexit.register( self.onExit_DeleteTmpFile )
        
        self.tmpFile = tmpFile
        self.tmpFileName = tmpFileName
        self.argv0 = self.tmpFileName


    def chdirOnInit(self):
        os.chdir( self.argv0Dir )
        return self
        
    def deleteTmpFile(self):
        if self.tmpFile!=None:
            self.tmpFile.close()
            fileNameToDelete = self.tmpFile.name
            assert fileNameToDelete.endswith( '.jocceasy.tmp.py' )
            try:
                os.remove( fileNameToDelete )
            except:
                #print( traceback.format_exc() )
                'pass'
            #print('deleteTmpFile func')
    @property
    def flib(self):
        return self.functionLibrary
    
    @property
    def magicConf(self):
        return self.MagicConf
        
    def loadCode(self):
        if self.argv0!=None and self.argv0!='':
            with open( self.argv0, 'r' ) as f:
                self.codeLoaded = f.read()
        return self

    def prep(self):
        self.chdirOnInit()
        

    def onExit_DeleteTmpFile(self, fileNameToDelete):
        self.deleteTmpFile()
        
    def recode(self, recodeRequiresMagicExit=None, forceRepeatReloadAndRecode=False):

        if forceRepeatReloadAndRecode:
            self.loadCode()
        
        if self._hasBeenRecoded and not forceRepeatReloadAndRecode:            
            return self.code  ## exit early if we've already been recode and not forcing
        
        if self.codeLoaded==None:
            self.loadCode()
        
        ## if there's still no loaded code even after
        ## lodeCode call, give up    
        if self.codeLoaded==None:
            self.code = ''
            return self
            
        ##get default behaviour from self
        if recodeRequiresMagicExit==None:
            recodeRequiresMagicExit = self.recodeRequiresMagicExit
        
        magicConf = self.magicConf
        mm = magicConf.marks
    
        code = self.codeLoaded
        lines = code.split('\n')
        codes = []
        codes.append( "'pass' ## this line ensures code is valid even if everything else is magic comments" )
        wasExitFound = False
        for i,line in enumerate(lines):
            if wasExitFound == False:
                if mm.exit in line:
                    wasExitFound = True
                continue
            else:
                if ('#' + '%D') in line:
                    doNothing=True
                elif line.lstrip().startswith( mm.callQuiet ):
                    marker = mm.callQuiet
                    line = self.filterLineRemoveLeadingMarker( line, marker )
                    line = self.filterLineCall( line, quiet=True )
                    codes.append(line)
                elif line.lstrip().startswith( mm.call ):                    
                    marker = mm.call
                    line = self.filterLineRemoveLeadingMarker( line, marker )
                    line = self.filterLineCall( line )
                    codes.append(line)
                elif line.lstrip().startswith( mm.lit ):
                    marker = mm.lit
                    line = self.filterLineRemoveLeadingMarker( line, marker )
                    line = self.filterLineLit( line )
                    codes.append(line)
                else:
                    codes.append(line)
        
        self.code = '\n'.join( codes )
        
        if wasExitFound==False:
            if recodeRequiresMagicExit==True:
                raise ValueError("The magic exit marker must exist")
            ## if it wasn't found, none of the translation will work
            ## so revert to code as it was
            self.code = self.codeLoaded
            
        self._hasBeenRecoded = True
        
        return self  ## useful for self.recode().code

    
    """
    def make_class(self, class_name, base_classes=(object,), methods_and_members=dict()  ):
        x = type( str(class_name), base_classes, methods_and_members )
        self.dynamic_classes[class_name] = x
        return x
    """
        
    def filterLineCall(self, line, quiet=False ):
        lineLStripped = line.lstrip()
        dif = len(line) - len(lineLStripped)
        linePreIndent = line[:dif]
        linePostIndent = line[dif:]
        callFuncCmdStr = ".Call("
        if quiet==True:
            callFuncCmdStr = ".CallQ(  "
        s = "tmpReturned = " + self.__class__.__name__ + callFuncCmdStr
        e = " , magicDict=locals()  ) "
        lineOut = linePreIndent + s + repr(linePostIndent) + e
        return lineOut
    
    ## delete this function    
    #def filterLineCallQuiet(self, line ):
    #    return self.filterLineCall(line, quiet=True)
    
    
    def filterLineLit(self, line ):
        lineOut = repr(line)
        return lineOut


    def filterLineRemoveLeadingMarker(self, line, marker):
        frags = line.split(marker,1)
        if len(frags)>1:
            frags[1] = frags[1].lstrip()
        lineOut = "".join(frags)
        return lineOut

    def getCode(self, doRecode=True, forceRecode=False, recodeRequiresMagicExit=None ):
        if self.codeLoaded==None:
            self.loadCode()
        ##get default behaviour from self
        if recodeRequiresMagicExit==None:
            recodeRequiresMagicExit = self.recodeRequiresMagicExit
        if self.code==None:
            if doRecode==True:
                self.code=self.codeLoaded
                #print(    'self.code length: ' + str( len(self.code) )    )
                if len(self.code)>0:
                    self.recode(recodeRequiresMagicExit=recodeRequiresMagicExit)
            else:
                self.code = self.codeLoaded        
        return self.code
        

## this can be checked to prevent circular imports
EasyModLoadingIsComplete=True
EasyModLoadingIsComplete=True
for cb in SelfModLoadingCompleteCallbacks:
    if False:
        ## *** todo, add check for callback type object with args and kwargs
        'pass'
    elif callable(cb):
        cb( SelfMod )
