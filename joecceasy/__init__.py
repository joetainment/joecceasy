## joecceasy module __init__.py
"""

Recommended way of importing, without magic, is:
from joecceasy import Easy

Recommended way of importing, with magic, is:
from joecceasy import Easy; exec(Easy.CodeQ); exit(); #%exit  
"""
from _ctypes import ArgumentError


"""
to do:
  add option to cd to script dir
  gather other useful info
  run commands super easy and get back output and errors easy
"""


import atexit, collections, datetime, importlib, inspect
import os, sys, subprocess, time, tempfile, traceback


from . import Utils
from .Utils import callInitClass, classproperty, classproperty, Object

from . import forbiddenfruit
forbiddenfruit.curse

GlobalSelfModule = __import__(__name__)

GlobalReloadWarning = r"""
Easy-reloading the Easy module now. Hopefully you used  exec(Easy.ReloadStr)  or  Easy=Easy.Reload()  or something else similar.  Warning, this should only be used for simple tests. Reloading is inherently tricky and bug prone in Python. Reloading the interpreter is usually a better option.
"""[1:-1]

#############################
#### Global Variables

GlobalMagic = Object()
GlobalMagic.marks = Object()
GlobalMagic.marks.lit = ('#'+'%lit')
GlobalMagic.marks.call = ('#'+'%call')
GlobalMagic.marks.callQuiet = ('#'+'%callq')
GlobalMagic.marks.callNoLit = ('#'+'%nolit%%')
GlobalMagic.marks.exit = ('#'+'%exit')

class Easy():
    ## Inst is the global easy access Singleton of the class
    __SingletonInstance = None
    __ReloadCount = 0
    __ReloadStr = r"""
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

    ###################################
    #### Class and static methods
    
    @classmethod
    def _SetReloadCount( cls, count ):
        cls.__ReloadCount = count 
        
    
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
    
    @classmethod
    def AbsPath(cls, path):
        return os.path.abspath(path)
    
    @classproperty
    def Args(cls):
        return sys.argv[1:]
        
    @classproperty
    def ArgsCount(cls):
        return len( sys.argv[1:] )

        
    @classmethod
    def Call( cls, args ):
        return cls.Inst.actionCall( args )
        
    @classmethod
    def CallInteractive( cls, args ):
        subprocess.run(
            args,
            shell=True
        )


    
    @classmethod
    def CallLoud( cls, args ):
        return cls.Inst.actionCall( args, loud=True )
   
    @classmethod
    def CallQ( cls, args ):
        return cls.Inst.actionCall( args, quiet=True )
         
    @classproperty
    def Code(cls, *args, **kargs):
        #print( 'Code is being processed and run by joeccbatpy... ' + cls.Inst.argv0 + '' )
        return cls.CodeQuiet
        
    @classproperty
    def CodeQ(cls, *args, **kargs):
        return cls.CodeQuiet
        
    @classproperty
    def CodeQuiet(cls, *args, **kargs):
        return cls.Inst.getCode()

    @classproperty
    def CurrentWorkDir( cls ):
        i = cls.Inst
        return os.getcwd()
        
    @classproperty
    def Cwd( cls ):
        return cls.CurrentWorkDir
        
    @classproperty
    def Easy(cls):
        return cls.CodeQuiet
        
    @classproperty
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
    def Magic(cls):
        return GlobalMagic

    @classproperty
    def Module(cls):
        return __import__( __name__ )
        
        
        
    
    
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
    def PrintTail( cls, args, numlines=4 ):
        r = "\n".join(  args.split('\n')[ -1-numlines :-1 ] )
        print( r )

    @classmethod
    def PrintWithFormat( cls, string0, *args, **kargs ):
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
                targetMod = __import( __name__ )
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
            print( f"Reload of Easy Module complete. Reload count is now: {count}" )
            return mod.Easy
        except Exception as e:
            if not quiet:
                print( traceback.format_exc() )
                print( "Reload of Easy Module failed." )
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
    
    def __init__(self): 
        self.cls=self.__class__
        self.recodeRequiresMagicExit=True
        self.origWorkDir = os.getcwd()
        self.code = None

        self.argv = sys.argv
        
        assert len(self.argv)>0
        self.argv0 = self.argv[0]
        
        assert type(sys.argv[0])==str
        
        self.tmpFile = None        
        self.tmpFileName = None
        
        if self.argv0=="":
            tmpFile = tempfile.NamedTemporaryFile(
                mode='r', suffix='.jocceasy.tmp.py', delete=False,
            )
            tmpFileName = os.path.realpath( tmpFile.name )
            atexit.register( self.onExit_DeleteTmpFile )
            
            self.tmpFile = tmpFile
            self.tmpFileName = tmpFileName
            self.argv0 =  self.tmpFileName
                
        else:
            self.argv0 = os.path.realpath(sys.argv[0])
            
        self.argv0Dir = os.path.dirname( self.argv0 )
        
        with open( self.argv0, 'r' ) as f:
            self.codeAtStartup = f.read()
        
        self.prep()      


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
    def magic(self):
        return self.Magic


    def prep(self):
        self.origWorkDir = os.getcwd()
        os.chdir( self.argv0Dir )
        return self
        
    def recode(self, recodeRequiresMagicExit=None):
        ##get default behaviour from self
        if recodeRequiresMagicExit==None:
            recodeRequiresMagicExit = self.recodeRequiresMagicExit
        
        magic = self.magic
        mm = magic.marks
    
        code = self.code
        lines = code.split('\n')
        codes = []
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
                    line = self.filterLineCallQuiet( line )
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
            self.code = self.codeAtStartup


    def getCode(self, forceRecode=False, recodeRequiresMagicExit=None ):
        ##get default behaviour from self
        if recodeRequiresMagicExit==None:
            recodeRequiresMagicExit = self.recodeRequiresMagicExit
        if self.code==None:
            self.code=self.codeAtStartup
            #print(    'self.code length: ' + str( len(self.code) )    )
            if len(self.code)>0:
                self.recode(recodeRequiresMagicExit=recodeRequiresMagicExit)        
        return self.code
        
    def filterLineCall(self, line ):
        lineLStripped = line.lstrip()
        dif = len(line) - len(lineLStripped)
        linePreIndent = line[:dif]
        linePostIndent = line[dif:]
        s = "tmpResult = " + self.__class__.__name__ + ".Call("
        e = " ) "
        lineOut = linePreIndent + s + repr(linePostIndent) + e
        return lineOut
        
    def filterLineCallQuiet(self, line ):
        s = "tmpResult = " + self.__class__.__name__ + ".CallQ("
        e = " ) "
        lineOut = s + repr(line) + e
        return lineOut

    def filterLineLit(self, line ):
        lineOut = line.replace( '\\', '\\\\' )
        return lineOut


    def filterLineRemoveLeadingMarker(self, line, marker):
        frags = line.split(marker,1)
        if len(frags)>1:
            frags[1] = frags[1].lstrip()
        lineOut = "".join(frags)
        return lineOut
        
    def actionCall(self, args, quiet=False, loud=False):
        if not quiet:
            if loud==True:
                print( '-------- Start of Call --------' )
                print( 'Calling: '+ args )
        r = subprocess.run(
            args,
            shell=True,
            text=True,
            #capture_output=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if not quiet:
            print( (r.stdout) )
            if loud==True:
                print( '-------- End Of Call --------' )
        return r