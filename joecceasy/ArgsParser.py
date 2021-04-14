import argparse
from . import Utils

"""
if using GetArg for positional args,
the argsparser dict internal key name for arg value will be
the key "argsParserPosZero"
the nargs keyword can be used to gather more than onenargs

short form will be auto added if not ambiguous

long forms will be made automatically, don't have to include "-" or "--"

when getting by name, don't include dashes either

str kinds default to ''
flag kind defaults to False
int kind defaults None


        
addFlag func
        useful kargs that can be passed:
          help type
"""
class ArgsParser():
    __SingletonInstance=None
    
    @Utils.Classproperty
    def Inst( cls ):
        if cls.__SingletonInstance==None:
            cls.__SingletonInstance=cls()
        return cls.__SingletonInstance
    
    @classmethod
    def GetFlag(cls,*args,**kargs):
        r = cls.Get(*args,kind='flag',**kargs)
        assert type(r)==bool
        return r
    @classmethod
    def GetFloat(cls,*args,**kargs):
        r = cls.Get(*args,kind='float',**kargs)
        assert type(r)==float
        return r
    @classmethod
    def GetInt(cls,*args,**kargs):
        r = cls.Get(*args,kind='int',**kargs)
        assert type(r)==int
        return r
    @classmethod
    def GetNs(cls,*args,**kargs):
        return cls.Inst.ns
    @classmethod
    def GetNargs(cls,*args,**kargs):
        r = cls.Get(*args,kind='nargs',**kargs)
        assert type(r)==list
        return r
    @classmethod
    def GetStr(cls,*args,**kargs):
        r = cls.Get(*args,kind='str',**kargs)
        assert type(r)==str
        return r
    def GetExisting(cls, argName, *args,**kargs):
        if argsParser is None:
            argsParser=cls.Inst
        return argsParser.get( argName, *args,**kargs)
    
    @classmethod
    def Get( cls, argName, *args, argsParser=None, kind='str',**kargs ):
        if kind=="flag":
            default=False
            if 'default' in kargs:
                del kargs['default']
        if kind=="str":
            default=''
            if 'default' in kargs:
                default = kargs['default']
                del kargs['default']
        if kind=="int":
            default=''
            if 'default' in kargs:
                default = kargs['default']
                del kargs['default']
        if kind=="nargs":
            ## nargs always overrites default with empty list
            default=[]
            if 'default' in kargs:
                del kargs['default']
        if kind=="float":
            default=''
            if 'default' in kargs:
                default = kargs['default']
                del kargs['default']
        """
        argName can be int 0 or "0" or 'argsParserPosZero'
        in order gather positional args
        nargs can be used to gather more
        
        extra args and kargs get passed to python's argumentparser's
        add_argument call
        """
        if argsParser is None:
            argsParser=cls.Inst
        isZero = argName==0 or argName=='0'
        if isZero or argName=='argsParserPosZero':
            assert argName==0
            argName='argsParserPosZero'
            if argName in argsParser.dictOfAlreadyAdded:
                return argsParser.get(argName) 
            else:
                assert kind!='flag'
                assert kind=='nargs' ## only str implemented so far                
                argsParser.addNargs( argName, *args, **kargs)
                return argsParser.get( argName )
                #raise Exception('positional args not implmented yet')
        else:
            if argName in argsParser.dictOfAlreadyAdded:
                return argsParser.get( argName )
            else:
                assert not argName.startswith('-')
                dashedArgName = "--" + argName
                if True==False:
                    pass
                elif kind=="int":
                    argsParser.addInt( dashedArgName, *args, **kargs)
                elif kind=="flag":
                    argsParser.addFlag( dashedArgName, *args, **kargs)
                elif kind=="float":
                    argsParser.addFloat( dashedArgName, *args, **kargs)
                elif kind=="str":
                    argsParser.addStr( dashedArgName, *args, **kargs)
                else:
                    raise Exception("this type not yet handled")
                return argsParser.get( argName )
            
            
    def __init__(self):
        self.dictOfAlreadyAdded = {}
        self.parser = argparse.ArgumentParser()
        self.needsReparse=True
        self._ns=None
        self._unknown=None
    @property 
    def ns(self):
        if self.needsReparse==True:
            self.reparse()
        return self._ns
    @property 
    def unknown(self):
        if self.needsReparse==True:
            self.reparse()
        return self._unknown
    
    def addStr(self, argName, *args, **kargs):
        if 'action' in kargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="store", type=str, default='',
            **kargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
        
    def addNargs(self, argName, *args, **kargs):
        if 'action' in kargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="extend", nargs='+', type=str, default=[],
            **kargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
    def addFloat(self, argName, *args, **kargs):
        if 'action' in kargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="store", type=float, default='',
            **kargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
    def addInt(self, argName, *args, **kargs):
        if 'action' in kargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="store", type=int, default='',
            **kargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
                
    def addFlag(self, argName, *args, **kargs):
        if 'action' in kargs:
            Exception(
                "Don't specify action, this func forces it to be 'store_true'"
            )        
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        #print(f"adding flag: {argName}")
        self.parser.add_argument( argName, *args,
                        action="store_true", default=False,
                        **kargs )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
        
    def get(self, argName):
        if argName=="0" or argName==0:
            argName='argsParserPosZero'
        return getattr( self.ns, argName )
    
    def reparse(self,*args,**kargs):
            ns, unknown = self.parser.parse_known_args( *args, **kargs )
            self._ns=ns
            self._unknown=unknown
            self.needsReparse = False                  