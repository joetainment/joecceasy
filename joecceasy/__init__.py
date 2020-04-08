"""

joecceasy python package __init__.py

Recommended way of importing, without magic, is:
from joecceasy import Easy

Recommended way of importing, with magic, is:
from joecceasy import Easy; exec(Easy.CodeQ); exit(); #%exit

to do:
  add option to cd to script dir
  gather other useful info
  run commands super easy and get back output and errors easy
"""

##################################################
##################################################
###### Imports

#################################
#### Python Standard Library imports
####
import atexit, collections, datetime, importlib, inspect
import os, sys, subprocess, time, tempfile, traceback
from _ctypes import ArgumentError


#################################
#### joeceasy module imports
####
from . import Utils
from .Utils import callInitCls, classproperty, classproperty, Object
from .ModulesLazyLoader import ModulesLazyLoader
## forbiddenfruit.curse for extension of built in classes
from . import forbiddenfruit


#### end of imports (non-dynamic ones at least)
##################################################
##################################################

###############################################
###############################################
######## Globals
####
##
#
GlobalSelfModule = __import__(__name__)

GlobalReloadWarning = r"""
Easy-reloading the Easy module now. Hopefully you used  exec(Easy.ReloadStr)  or  Easy=Easy.Reload()  or something else similar.  Warning, this should only be used for simple tests. Reloading is inherently tricky and bug prone in Python. Reloading the interpreter is usually a better option.
"""[1:-1]

GlobalReloadStr = r"""
import traceback
try:
  if 'Easy' in locals():
    from joecceasy import Easy
    Easy.Reload( )
except:
  print(  traceback.formatExc()  )

try:
  from joecceasy import Easy
  E = Easy
except:
  print(  traceback.formatExc()  )
"""

GlobalMagicConf = Object()
GlobalMagicConf.marks = Object()
GlobalMagicConf.marks.lit = ('#'+'%lit')
GlobalMagicConf.marks.call = ('#'+'%call')
GlobalMagicConf.marks.callQuiet = ('#'+'%callq')
GlobalMagicConf.marks.callNoLit = ('#'+'%nolit%%')
GlobalMagicConf.marks.exit = ('#'+'%exit')



#################################
#### Easy class (and metaclass)
####

class EasyMeta(type):
    
    @property
    def P(cls):
        return getattr( cls, '_P', None)
    @P.setter
    def P(cls, v):
        setattr( cls, '_P', v )
        print( v )
    def P_Clear(cls):
        delattr( cls, '_P')    
    
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
    __ReloadStr = GlobalReloadStr




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

    @classmethod
    def AbsPath(cls, path):
        return os.path.abspath(path)
            
    
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
        raise Exception(
            r'''Easy Arg0 function doesn't exist. '''
            '''You probably wanted to use the Argv0 function, '''
            '''note the "v" in the name.'''
        )
        
    @classproperty
    def Args(cls):
        return sys.argv[1:]
        
    @classproperty
    def ArgsCount(cls):
        return len( sys.argv[1:] )
    
    @classproperty
    def ArgsE(cls):
        return cls.EnumArgs()
        
    @classmethod
    def Call( cls, *args, **kargs ):
        return cls.Inst.actionCall( *args, **kargs )
        
    @classmethod
    def CallInteractive( cls, *args, **kargs ):
        kargs['interactive']=True
        cls.Inst.actionCall( *args, **kargs )
        
    
    @classmethod
    def CallLoud( cls, *args, **kargs ):
        kargs['loud']=True
        return cls.Inst.actionCall( *args, **kargs )
   
    @classmethod
    def CallQ( cls, *args, **kargs ):
        kargs['quiet']=True
        return cls.Inst.actionCall( *args, **kargs )
         
    @classproperty
    def Code(cls): ## property can't pass *args, **kargs
        #print( 'Code is being processed and run by joeccbatpy... ' + cls.Inst.argv0 + '' )
        return cls.CodeQuiet
        
    @classproperty
    def CodeQ(cls):  ## property can't pass *args, **kargs
        return cls.CodeQuiet
        
    @classproperty
    def CodeQuiet(cls):  ## property can't pass *args, **kargs
        return cls.Inst.getCode()

    @classproperty
    def CurrentWorkDir( cls ):
        return cls.GetCwd()
    
    @classmethod
    def GetCwd( cls ):
        i = cls.Inst
        return os.getcwd()
    
    @classmethod
    def Getcwd( cls ):  ## just an alternative capitalization
        return cls.GetCwd()
    
        
    @classproperty
    def Cwd( cls ):
        return cls.GetCwd()
        
    @classproperty
    def Easy(cls):
        return Easy.Magic
    
    @classmethod
    def EnumArgs(cls):
        return enumerate( sys.argv[1:] )
        
    @classmethod
    def ExtendBuiltinClass(cls, clsArg, callFunc, callName=None ):
        if callName == None:
            callName = callFunc.__name__
        return forbiddenfruit.curse( clsArg, callName, callFunc )
    
    @staticmethod
    def Fstring( stringToEval ):
        """
        Returns a python fstring literal, which will eval
        to result as what an actual fstring would.
        
        Use with eval to create Fstring dynamically.
        (It's sort of like "late binding" a string as an fstring)
        
        usage example:
        
        number = 5
        example = "the number is: {number}"
        result = eval( Easy.Fstring( example ) )
        
        result will end up containing 5 at the end of its text, as
        if you wrote an Fstring as: result=f"the number is: {number}"
        
        """
        return "f"+ repr(stringToEval)
    
    
    @staticmethod
    def Format( *args, **kargs ):
        args=list(args)
        hasError=False
        if args!=None:
            if len(args)>0:
                string0=args.pop(0)
                return string0.format( *args, **kargs )
            else:
                hasError=True
        else:
            hasError=True
        if hasError==True:
            raise TypeError( "string required as first argument to this Format function" )

    @staticmethod
    def FormatV( string0, args=None, kargs=None ):
        if args==None:
            args=[]
        if kargs==None:
            kargs={}
        #print(kargs)
        return string0.format( *args, **kargs )
        
    @staticmethod
    def GetRoutinesFromObj(sourceObj):
        l=inspect.getmembers( sourceObj, inspect.isroutine)
        result=[]
        for iname, i in l:
            i.__name__=iname
            print( i.__name__ )
            result.append (i)
        return result

    @staticmethod
    def Import(modname, byFilePath="unimplemented"):
        return importlib.import_module( modname )
        
    @classmethod
    def ImportFile( cls, path, asName= None, relativeToScript = "unimplemented" ):
        fileName=path.split(os.sep)[-1]
        if asName== None:
            asName = fileName[:-3]
        spec = importlib.util.spec_from_file_location( asName, path )
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    
    
    @classmethod
    def IncrementReloadCount(cls): 
        cls.__ReloadCount += 1
        return cls
    
    @classmethod
    def Init(cls):
        """
        Auto Initializes the Easy module with default Easy Options
        Does things like change working dir.
        """
        if cls.__SingletonInstance==None:
            cls.__SingletonInstance = cls(
                shouldAutoInit=True,
                shouldAutoChdirToArg0Dir=True,
                shouldAutoLoadCode=True,
            )
        else:
            cls.__SingletonInstance.init()
            
        return cls.__SingletonInstance
    
    @classproperty
    def Inst(cls):
        if cls.__SingletonInstance==None:
            cls.__SingletonInstance = cls()
        return cls.__SingletonInstance
    
    @Inst.setter
    def InstSetter( cls ):
        #print( 'no setter available' )
        raise AttributeError("Can't assign to readonly Inst property")

    
    ## We call it "Magic" because it triggers all kinds of background
    ## stuff to happen.  Magic often implies that
    ## in common coder terminologys
    @classproperty   
    def Magic(cls):
        cls.Init()
        return cls.Inst.getCode()

    @classproperty
    def MagicConf(cls):
        return GlobalMagicConf

    @classproperty
    def Mods(cls):
        return cls.Inst.modules

    @classproperty
    def Module(cls):
        return __import__( __name__ )
        
    
    @classproperty
    def Modules(cls):
        return cls.Inst.modules    
        
    
    
    @classmethod
    def NowUtc(cls):
        return datetime.datetime.utcnow()
    @classmethod
    def NowAsUtc(cls):
        return cls.NowUtc()
    
    @classmethod
    def NowAsLocal(cls):
        return cls.NowLocal()
        
    @classmethod
    def NowLocal(cls):
        localTimeZone=cls.TzLocal()
        return datetime.datetime.now( tz=localTimeZone )
        #or a one-liner
        """
        return datetime.datetime.now(
                tz=datetime.timezone(
                    datetime.datetime.now() -
                        datetime.datetime.utcnow()
                )
        """
    @classmethod
    def NowLocalStr(cls, fmt=None, style=None):
        if fmt is None:
            fmt = "y%Ym%md%dh%Hn%Ms%SAsLocalTime"
            if style==None:
                'pass'
            else:
                'pass'
        return cls.NewLocal().strftime(fmt)

    
    @classmethod
    def ODict(cls, *args,**kargs):
        return collections.OrderedDict( *args, **kargs )


    @classproperty
    def OrigWorkDir( cls ):
        return cls.Inst.origWorkDir
   
        
    @classmethod
    def PrintTail( cls, *args, **kargs ):
        """
        Print the last n lines of each argument.
        
        Can pass
        """
        tailsep = kargs.get( 'tailsep', '\n\n' )
        asList = kargs.get( 'asList', None )        

        kargs['asList']=True ## set option for call to cls.Tail
        tails = cls.Tail( *args, **kargs )
        

        ## prep kargs for print
        kargs.pop( 'tailsep', None )
        kargs.pop( 'asList', None )
        kargs.pop( 'n' )
        
        ##print them
        for i,t in enumerate(tails):
            if tailsep!=None:
                if i>0:
                    print( tailsep, end='' )
            print( t, **kargs )
                
        if asList:
            return tails
        else:
            s = tailsep.join( tails )
            return s 

    @classmethod
    def PrintWithFormat( cls, string0, *args, **kargs ):
        """
        Print and formats a single given string argument.
        Other arguments will be passed to format function.
        """
        s = cls.Format( string0, *args,**kargs)
        print(s)
        return s
    
    @classmethod
    def PrintWithFormatV( cls, string0, args=None, kargs=None, sep=' ', end='\n' ):
        s = cls.FormatV(string0,  args, kargs )
        print(s, sep=sep, end=end )
        return s

    @classmethod
    def TrimAndTab( cls, st ):
        st = cls.TrimLines(st)
        #print(st)
        lines = st.split('\n')
        assert( len(lines)>1)
        line0=lines[0]
        assert( '#' in line0 )
        line0s = line0.lstrip()
        #print( line0s )
        assert( line0s.startswith('#') )
        startindex = line0.index('#')
        fixedLines = []
        for line in lines[1:]:
            fix = line[startindex:]
            fixedLines.append(fix)
        r = '\n'.join( fixedLines ) 
        return r
    
    @classmethod
    def TrimLines( cls, st ):
        lines = st.split('\n')
        assert(  len(lines) > 2  )
        assert( lines[0].strip()=='' )
        assert( lines[-1].strip()=='' )
        r = '\n'.join( lines[1:-1] )
        return r


    """
    @classmethod
    def TrimTodo( cls, st ):
        return st
    """    
         
                              
    @staticmethod
    def ReloadModule( targetModule=None, name=None):
        print( GlobalReloadWarning )
        try:
            if targetMod==None:
                targetMod = __import__( __name__ )
            mod = importlib.reload( targetMod )
            return mod
        except:
            print( traceback.format_exc() )
            return GlobalSelfModule
            
    @classproperty
    def ReloadStr( cls ):
        return cls.__ReloadStr
    
    @classmethod
    def Reload( cls, quiet=False ):
        if not quiet:
            print(GlobalReloadWarning)
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
                print( traceback.format_exc() )
                print( "Reload of Easy module failed." )
                return GlobalSelfModule.Easy
            raise( e )
        
    
    
    @classproperty
    def ReloadCount(cls): 
        return cls.__ReloadCount
    

    @classproperty
    def ScriptDir( cls ):
        return cls.Inst.argv0Dir
    
    
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
    def Tail( cls, *args, **kargs ):
        argsList = list(args) ##
        n = kargs.pop( 'n', 5 )
        tailsep = kargs.pop( 'tailsep', '\n\n' )
        asList=kargs.pop( 'asList', False )
        
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
    def Traceback(cls):
        return traceback.format_exc()
        
    @classmethod
    def TzOff(cls):
        now=datetime.datetime.now()
        utcnow=datetime.datetime.utcnow()
        offset=now - utcnow
        return offset
        
    @classmethod
    def TzLocal(cls):
        return datetime.timezone( cls.TzOff() )    

       
    @classproperty
    def Utils(cls):
        return Utils




    ##################################
    #### Instance Methods and Properties
    
    def __init__(self,
            shouldAutoInit=False,
            shouldAutoChdirToArg0Dir=False,
            shouldAutoLoadCode=False,
            shouldAutoRecode='unimplemented'
        ):
        
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
        self.modules = ModulesLazyLoader()
        
        


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


    def atInitFallbackInCaseNoArg0(self):
        tmpFile = tempfile.NamedTemporaryFile(
            mode='r', suffix='.jocceasy.tmp.py', delete=False,
        )
        tmpFileName = os.path.realpath( tmpFile.name )
        atexit.register( self.onExit_DeleteTmpFile )
        
        self.tmpFile = tmpFile
        self.tmpFileName = tmpFileName
        self.argv0 = self.tmpFileName


    def onExit_DeleteTmpFile(self, fileNameToDelete):
        self.deleteTmpFile()
        
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
    def magicConf(self):
        return self.MagicConf


    def prep(self):
        self.chdirOnInit()
        
    def chdirOnInit(self):
        os.chdir( self.argv0Dir )
        return self

    def loadCode(self):
        if self.argv0!=None and self.argv0!='':
            with open( self.argv0, 'r' ) as f:
                self.codeLoaded = f.read()
        return self
        
        
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
        
    def actionCall(self, argsForCommandLine, magicDict=None, quiet=False, loud=False, interactive=False):

        if magicDict!=None:
            for k, v in magicDict.items():
                mkey = '#%' + k + '%#'
                if mkey in argsForCommandLine:
                    argsForCommandLine = (
                        argsForCommandLine.
                            replace(
                                mkey,
                                str(v)
                            )
                        )
        
        if interactive==True:
            subprocess.run(
            argsForCommandLine,
            shell=True
        )

        
        if not quiet:
            if loud==True:
                print( '-------- Start of Call --------' )
                print( 'Calling: '+ argsForCommandLine )
                
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
        


