from . import Utils

Funcs = Utils.Funcs
classproperty = Utils.classproperty

class AbstractBaseClass:
    """
    This class simply has some functionality we often
    want on typical classes, such as ontoDict and ontoSelf
    extend this as a habit when making new classes in apps etc
    
    for init and passing through kwargs intelligently/flexibly, use
    a pattern like...
        def __init__(
            self,
            *args,
            **kwargs,
            ):
            
            kwargs = self.kwargsViaDict( kwargs,
                 
                'title':"EasyLauncher",
                'minimumHeight':450,
                'example1':True,
                'example2':False,
                
                ## now control which get also applied to self
                filterOutput={
                    'example1','example2'
                }

            )
            
            
        
            kwargs = self.kwargsViaDict( kwargs, { 
                'title':"EasyLauncher",
                'minimumHeight':450,
                'kwarg1-AddedViaKwargsViaDict':True,
                'kwarg2-AddedViaKwargsViaDict':False,
            })
            ## will modify both kwargs and self via it's attribute dict if given one,
            ## otherwise won't modify kwargs but will
            ## apply the ones in the filter to the object
            self.kwargsOntoSelf(  
                kwargs,
                {   ## keys/values to be added to kwargs
                    'kwarg3-AddedViaAttrDict':True,
                    'kwarg4-AddedViaAttrDict':False,
                },
                
                ## attributes from kwargs to apply to self
                filterInput={ ## only apply these keys from kwargs to self
                    ## actual value is ignored is filterOutput is dict
                    'kwarg1-AddedViaKwargsViaDict':1,
                    'kwarg2-AddedViaKwargsViaDict':1,
                },                    
            )
            self.kwargsOntoSelf(
                None,  #not given kwargs as dest dict, just attr dict
                {
                    'kwarg5-AddedViaAttrDict':True,
                    'kwarg6-AddedViaAttrDict':False,
                }
            )
            self.dictOntoSelf( {
                'launcherColumns':7,
                'pathOfShortcuts':DEFAULT_PATH,               
            })
            superKwargs = self.dictCopyExclusive( kwargs, "minimumHeight" )           
            super().__init__( *args, **superKwargs
            ) 
        
    
    
    """
    @property
    def kwargsD(self):
        return self.kwargsViaDict
    def kwargsViaDict(self, destDict, defaultsDict, *args, **kwargs):
        ## this swaps order of first two args in func call because it's way more intuitive
        ## when func is used in this manner
        return Funcs.OntoDict( *args, defaultsDict, destDict,  **kwargs )
    def kwargsViaDictWithBackup(self, destDict, defaultsDict, *args, **kwargs):
        return Funcs.OntoDictWithBackup( defaultsDict, destDict, *args, **kwargs )
    def kwargsOntoObj(self, *args, **kwargs):
        return Funcs.OntoDict( *args, **kwargs )
    def kwargsOntoSelf(self, *args, **kwargs):
        return Funcs.OntoObj( self, *args, **kwargs )
    def dictOntoSelf(self, *args, **kwargs):
        return Funcs.OntoObj(
            ## args below will be
            ## self, None meaning no default dict, first arg of *args as attrDict
            self,    None,  *args, **kwargs                      
        )
    def dictCopyExclusive(self, *args, **kwargs ):
        return Funcs.DictCopyExclusive( *args, **kwargs )
    
    @classproperty
    def Easy(cls):
        import Easy
        return Easy
    @classproperty
    def EasyFuncs(cls):
        return Funcs