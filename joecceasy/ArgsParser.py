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
        useful kwargs that can be passed:
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
    def GetFlag(cls,*args,**kwargs):
        r = cls.Get(*args,kind='flag',**kwargs)
        assert type(r)==bool
        return r
    @classmethod
    def GetFloat(cls,*args,**kwargs):
        r = cls.Get(*args,kind='float',**kwargs)
        assert type(r)==float
        return r
    @classmethod
    def GetInt(cls,*args,**kwargs):
        r = cls.Get(*args,kind='int',**kwargs)
        assert type(r)==int
        return r
    @classmethod
    def GetNs(cls,*args,**kwargs):
        return cls.Inst.ns
    @classmethod
    def GetNargs(cls,*args,**kwargs):
        r = cls.Get(*args,kind='nargs',**kwargs)
        assert type(r)==list
        return r
    @classmethod
    def GetStr(cls,*args,**kwargs):
        r = cls.Get(*args,kind='str',**kwargs)
        assert type(r)==str
        return r
    def GetExisting(cls, argName, *args,**kwargs):
        if argsParser is None:
            argsParser=cls.Inst
        return argsParser.get( argName, *args,**kwargs)
    
    @classmethod
    def Get( cls, argName, *args, argsParser=None, kind='str',**kwargs ):
        if kind=="flag":
            default=False
            if 'default' in kwargs:
                del kwargs['default']
        if kind=="str":
            default=''
            if 'default' in kwargs:
                default = kwargs['default']
                del kwargs['default']
        if kind=="int":
            default=''
            if 'default' in kwargs:
                default = kwargs['default']
                del kwargs['default']
        if kind=="nargs":
            ## nargs always overrites default with empty list
            default=[]
            if 'default' in kwargs:
                del kwargs['default']
        if kind=="float":
            default=''
            if 'default' in kwargs:
                default = kwargs['default']
                del kwargs['default']
        """
        argName can be int 0 or "0" or 'argsParserPosZero'
        in order gather positional args
        nargs can be used to gather more
        
        extra args and kwargs get passed to python's argumentparser's
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
                argsParser.addNargs( argName, *args, **kwargs)
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
                    argsParser.addInt( dashedArgName, *args, **kwargs)
                elif kind=="flag":
                    argsParser.addFlag( dashedArgName, *args, **kwargs)
                elif kind=="float":
                    argsParser.addFloat( dashedArgName, *args, **kwargs)
                elif kind=="str":
                    argsParser.addStr( dashedArgName, *args, **kwargs)
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
    
    def addStr(self, argName, *args, **kwargs):
        if 'action' in kwargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="store", type=str, default='',
            **kwargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
        
    def addNargs(self, argName, *args, **kwargs):
        if 'action' in kwargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="extend", nargs='+', type=str, default=[],
            **kwargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
    def addFloat(self, argName, *args, **kwargs):
        if 'action' in kwargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="store", type=float, default='',
            **kwargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
    def addInt(self, argName, *args, **kwargs):
        if 'action' in kwargs:
            Exception(
                "Don't specify action, this func forces it to be 'store'"
            )
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        self.parser.add_argument( argName, *args,
            action="store", type=int, default='',
            **kwargs
        )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
                
    def addFlag(self, argName, *args, **kwargs):
        if 'action' in kwargs:
            Exception(
                "Don't specify action, this func forces it to be 'store_true'"
            )        
        assert type(argName)!=int
        assert type(argName)!=float
        assert argName not in self.dictOfAlreadyAdded
        #print(f"adding flag: {argName}")
        self.parser.add_argument( argName, *args,
                        action="store_true", default=False,
                        **kwargs )
        self.dictOfAlreadyAdded[argName]=True
        self.needsReparse=True
        
    def get(self, argName):
        if argName=="0" or argName==0:
            argName='argsParserPosZero'
        return getattr( self.ns, argName )
    
    def reparse(self,*args,**kwargs):
            ns, unknown = self.parser.parse_known_args( *args, **kwargs )
            self._ns=ns
            self._unknown=unknown
            self.needsReparse = False                  