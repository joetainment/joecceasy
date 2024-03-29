"""
Standalone utilities that don't rely on other
Non-Python-standard imports
Aside from any custom-imports of Utils* submodules module
Which should follow similar dependency rules

This module is one of the first things imported by joecceasy
And should not circularly import it or other things

as a general rule, this module should be safe to import
with confidence, knowing that its import alone won't run
any code other than code that defines classes, functions,
and maybe some really basic variables

pretty much everything done in this file is done inside
of the functions or classes. Global vars set are only
UtilsModLoadingIsComplete and a bunch of aliases
for the functions and classes

todo:
  map like features but made easier and clearer for instances
    getattr type calls working on instance methods by string name
    (mostly already done now)
  zip like features but made easier and clearer
    employee_names, employee_numbers = zip(*employees_zipped)
    #--and-#
    for name, number in zip(employee_names, employee_numbers):
        print(name, number)
        

"""
## Here we explicitly do not import anything
## immediately. Not builtins, and nothing
## like SelfMod or SelfPak or Easy
## because we want to avoid triggering any code
## to run
##
## Most vars made are just aliases for
## functions and classes
##
## The only global var that isn't an alias is:
##  UtilsModLoadingIsComplete, which get set True
##  at end of this file
UtilsModLoadingIsComplete=False
##
####################################################
## raw functions that can't be part of class

JoecceasyMagicMarker20220206918745738 = (
  "JoecceasyMagicMarker20220206918745738__"
 +"opts_begin_files_only__marker__"
 +"every_opt_after_this_is_an_intentional_filename"
 +"_even_if_it_starts_w_dash"
)

def seePrint( var, val,   sep=' ',end='\n', 
              withType=True, withTime=False, withNonRepr=False,
              spcs='    '
    ):  
    #prefix="see| ", #print( prefix, end='')
    ls = [
            var, '=',
           repr(val), spcs,
    ]
    if withType:
        ls.extend([
            'type:', type(val), spcs,
        ])
    if withTime:
        t = datetime.datetime.now(),
        ls.extend([ 'time:', spcs,  ])
    if withNonRepr:  ## nonrepr section
        strVal=str(val)
        ls.extend( [
            '\n'+var+sep+
            "=      ## as str not repr, shown on next lines\n"+
            strVal,
        ])
        """
        if '\n' in strVal:
            nonrepr = '\n'+'non-repr:'+'\n'
            ls.extend( [ nonrepr + strVal,])
        else:
            nonrepr = 'non-repr:'
            ls.extend( [ nonrepr, strVal,])
        """
    tup=tuple(ls)
    print( *tup,
           sep=sep, end=end
    )

def ic(*args,sep=' ', end='\n', **kwargs):  #iccKwargs={}
    import datetime, inspect, re
    frame = inspect.currentframe().f_back
    s = inspect.getframeinfo(frame).code_context[0]
    r = re.search(r"\((.*)\)", s).group(1)
    vnames = r.split(", ")
    retval=None
    for i,(var,val) in enumerate(zip(vnames, args)):
        seePrint(var,val,sep=sep,end=end)
        if i==0:
            retval=val
    return retval

def see(*args, sep=' ', end='\n', **kwargs):
    import sys
    frame = sys._getframe(1)
    argsList=list(args)
    i=0
    try:
        assert isinstance( argsList[0], int )
        verbosity = argsList.pop(0)
        if verbosity > 0:
            withNonRepr=True
        else:
            withNonRepr=False
    except:
        withNonRepr=False
    ## recursively expand lists
    retval=None
    retvalHasBeenGrabbed=False
    while i < len(argsList):
        arg = argsList[i]
        expression = arg
        if isinstance( arg, str ):
            evaled=eval(expression, frame.f_globals, frame.f_locals)
            if not retvalHasBeenGrabbed:
                retval=evaled
                retvalHasBeenGrabbed=True
            seePrint( expression, evaled, sep=sep,end=end,
                withNonRepr=withNonRepr )
        else:
            try:
                argsList[i+1:i+1]=arg
            except:
                try:
                    argToInsert = str(arg)
                    assert isinstance(str, argToInsert)
                    argsList.insert(i+1, argToInsert )
                except:
                    print( "    Easy.See could not parse expression. Check to ensure it is a string or quoted literal string.    ", end=end)
        i+=1
    return retval



## A simpler alternative to using metaclasses
## not really needed much since we mostly use metaclasses instead
def CallInitCls( cls ):
    cls.InitCls()
    return cls
callInitCls=CallInitCls


#################################
#### Decorators

## classproperty only works for getters
## to make read/write work use @property properties
## on a metaclass instead 
## is named all lower case to match python's builtins
class classproperty(property):
        def __get__(self, obj, objtype=None):
            return super(classproperty, self).__get__(objtype)
        def __set__(self, obj, value):
            super(classproperty, self).__set__(type(obj), value)
        def __delete__(self, obj):
            super(classproperty, self).__delete__(type(obj))
## Some extra names for matching naming convensions
Classproperty=classproperty
ClassProperty=classproperty
ClassMethod=classmethod
Classmethod=classmethod



##############################################
#### Utility Classes

class Object(object):
    pass

class KwargsAsObj(object):
    def  __init__( self, *args, **kwargs ):
        d = self.__dict__
        for k in kwargs:
            d[k] = kwargs[k]

class EasyReturnedTimeout:
    def __str__(self):
        return ""
    #def __repr__(self):
    #    return repr("")
    """
    this should only ever be used by easy functions that timeout
    and have no altenative exception
    """
    
class EasyExplicitUnsetKwarg:
    """
    this is used in functions where we need to differentiate
    between a kwarg being intentionally None versus being
    unset
    """
    pass

    

class FunctionLibrary( ):
    def __init__(self):
        self.d = {}
    def add( self, func ):
        #  def addFunctionByName(self, func ):
        #print( f"func is: {func} of type {type(func)}")
        n = func.__name__
        assert n not in self.d
        assert n is not None
        assert n != ''
        self.d[func.__name__] = func
        return func
    def get(self, name):
        return self.d[name]



class CaseInsensitiveDict(dict):
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._convert_keys()
    def __getitem__(self, key):
        return super().__getitem__(self.__class__._k(key))
    def __setitem__(self, key, value):
        super().__setitem__(self.__class__._k(key), value)
    def __delitem__(self, key):
        return super().__delitem__(self.__class__._k(key))
    def __contains__(self, key):
        return super().__contains__(self.__class__._k(key))
    def has_key(self, key):
        return super().has_key(self.__class__._k(key))
    def pop(self, key, *args, **kwargs):
        return super().pop(self.__class__._k(key), *args, **kwargs)
    def get(self, key, *args, **kwargs):
        return super().get(self.__class__._k(key), *args, **kwargs)
    def setdefault(self, key, *args, **kwargs):
        return super().setdefault(self.__class__._k(key), *args, **kwargs)
    def update(self, E={}, **F):  ## there was comment about E being None by default
        super().update(self.__class__(E))
        super().update(self.__class__(**F))
    def _convert_keys(self):
        for k in list(self.keys()):
            v = super().pop(k)
            self.__setitem__(k, v)

            
class Funcs(object):
    """
    Stateless functions that don't depend on anything in Easy class,
    but that may depend on each other, and Utils raw funcs,
    or anything else imported into this Utils mod!

    Generally,this is all stuff that should not rely on any
    potentially cyclic or complex imports.
    """
    ## todo *** add options for including arbitrary pre and post lists

    @classmethod
    def AbsPath(cls, path):
        import os
        return os.path.abspath(path)
    
    @classmethod
    def AnyStartsWithAny(cls, haystackIter, needlesIter ):
        wasFound=False
        doBreak=False
        #print( haystackIter)
        #print( needlesIter)
        for h in haystackIter:
            #print( needlesIter)
            for n in needlesIter:
                #print( f'h: {h}  n: {n}')
                if h.startswith( n ):
                    doBreak=True
                    wasFound=True
                if doBreak:
                    break
            if doBreak:
                break
        return wasFound
    
    @classmethod
    def AnyEndsWithAny(cls, haystackIter, needlesIter ):
        wasFound=False
        doBreak=False
        #print( haystackIter)
        #print( needlesIter)
        for h in haystackIter:
            #print( needlesIter)
            for n in needlesIter:
                #print( f'h: {h}  n: {n}')
                if h.endswith(n):
                    doBreak=True
                    wasFound=True
                if doBreak:
                    break
            if doBreak:
                break
        return wasFound

    @classmethod
    def AnyEqualsAny( cls, haystackIter, needlesIter ):
        wasFound=False
        doBreak=False
        #print( haystackIter)
        #print( needlesIter)
        for h in haystackIter:
            #print( needlesIter)
            for n in needlesIter:
                #print( f'h: {h}  n: {n}')
                if h == n:
                    doBreak=True
                    wasFound=True
                if doBreak:
                    break
            if doBreak:
                break
        return wasFound
        
    @classmethod
    def AnyFuncOnAny( cls, haystackIter, needlesIter, func ):
        raise "not implemented"
    
    @classmethod
    def AnyOnAny( cls, haystackIter, needlesIter, funcOrFuncName ):
        if callable(funcOrFuncName):
            return cls.AnyOnAnyByFunc(
                haystackIter, needlesIter, funcOrFuncName )
        else:
            return cls.AnyOnAnyByMethod(
                haystackIter, needlesIter, funcOrFuncName )
            
    @classmethod
    def AnyOnAnyByFunc( cls, haystackIter, needlesIter, func, swap=False ):
        """
        swap will swap the order of haystack and needle in the function call
        """
        ## disabled, doing at function call avoids immutable dups
        #if swap:
        #    haystackIter, needlesIter = needlesIter, haystackIter
        wasFound=False
        doBreak=False
        for h in haystackIter:
            for n in needlesIter:
                if swap:
                    test = func( h, n )
                else:
                    test = func( n, h )
                if test:
                    doBreak=True
                    wasFound=True
                if doBreak:
                    break
            if doBreak:
                break
        return wasFound
    
    @classmethod
    def AnyInAny( cls, needlesIter, haystackIter ):
        wasFound=False
        doBreak=False
        #print( haystackIter)
        #print( needlesIter)
        for h in haystackIter:
            #print( needlesIter)
            for n in needlesIter:
                #print( f'h: {h}  n: {n}')
                if n in h: ## note, 'in' order opposite of most funcs
                    doBreak=True
                    wasFound=True
                if doBreak:
                    break
            if doBreak:
                break
        return wasFound
        
    @classmethod
    def AnyHaveAnyIn( cls, haystackIter, needlesIter ):
        """
        Same as AnyInAny but order of args are swapped
        so that the order matches the more common function calling order
        where haystack is given before needle
        """
        return cls.AnyInAny( needlesIter, haystackIter )
    
    
        #if useSets:
        #    it = set( haystackIter ).intersect( needlesIter )
        #    return bool( it ))
        #else:    
    
    
    
    @classmethod
    def AppendOrConcatWithLastStr( cls, ls, s ):
        if not isinstance( s, str ):
            ls.append( s )
        elif len(ls)<1:
            ls.append( s )
        else:
            lastItem = ls[-1]
            if not isinstance( lastItem, str ):
                ls.append( s )
            else:
                ## if we made it here, lastItem
                ##   is str like and
                ##   s is also string like
                lastItem = lastItem + s
                ls[-1] = lastItem
        return ls
    

    @classmethod
    def ApplyBackspace( cls, s,
            protectNewlines=True
        ):
        return cls.ApplyBackspaces( s )
    
    @classmethod
    def ApplyBackspaces(
            cls, s, protectNewlines=True
        ):
        """cancel literal backspaces and the characters 
           preceeding them from a string
        """
        #print('applying backspaces')
        import re

        while True:
            preLen = len(s)
            if protectNewlines:
                ## wipe out all backspaces right
                ## after newlines
                while True:
                    t = re.sub(
                        '\n\b', '\n',
                        s, count=999
                    )
                    if len(s) == len(t):
                        s=t
                        break
                
            #### at this point
            #### s should have all backspaces after
            ## newlines removed
            # if you find a character followed by a backspace, remove both
            # just once
            t = re.sub('.\b', '', s, count=1)
            s=t
            
            ## at this point if we've made any changes we have to
            ## repeat the cycle since removing backspaces may have
            ## reintrocued newlines
            ## thus, we can only break if no changes
            if len(s)==preLen:
                break
            
        ## at this point, the cycle of removing all \n\b then
        ## should of repeated until it stopped making any changes
        ## there should be no backspaces left except for at start of string
        ## now remove any backspaces from beginning of string
        s = re.sub('\b+', '', t)
        ## string should now have no backspaces
        return s

    @classproperty
    def Args(cls):
        import sys
        return sys.argv[1:]

    @classproperty
    def ArgsCount(cls):
        import sys
        return len( sys.argv[1:] )

    @classproperty
    def ArgsAsOpts(cls, *args, **kwargs ):
        return cls.ArgsToOpts( *args, **kwargs )
        
    @classmethod
    def ArgsToOpts(cls, args = None, doMarkFilesOnlyPoint=False ):
        """
        A very simple low effort way to get options
          option=lenny or --option=call will work
          or --option=carl  or 
          
          individual flags like  install or  --install
          will work two and show with value int(1) in dict
          
          "--" support exists and will put those in at the end of the dict
          
          should add function here from collapsing long and short forms
          after key startswith
            JoecceasyMagicMarker20220206918745738
            all remaining should be treated as files  
        """
        import sys
        from collections import OrderedDict
        if args is None:
            args = sys.argv[1:]
        
        iterArgs = iter(args)  ## not necessary if we don't allow space after equals
        opts = OrderedDict()
        singles = []
        pairs = []
        filesOnly = []
        reachedOnlyFileArgs=False
        for arg in iterArgs:
          if arg == '--':
            reachedOnlyFileArgs = True
            if doMarkFilesOnlyPoint:
                opts[JoecceasyMagicMarker20220206918745738]=True
          if reachedOnlyFileArgs == True:
            filesOnly.append( arg )
                
                
          else:
            if not '=' in arg:
              singles.append(arg)
            elif arg.startswith('='):
              ## have to treat as single arg
              singles.append(arg)
            else:
              splt = arg.split('=',1)
              if len(splt) != 2:
                singles.append(arg)
              else:
                spltA, spltB = splt
                pairs.append( [spltA, spltB ] )
        
        for el0,el1 in pairs:
          opts[el0]=el1
        
        for el in singles:
          opts[el]=1
        
        for el in filesOnly:
          opts[el]=2
          
        return opts
    
        ## Could hace code to handle pairs without spaces or
        ## spaces after equals signs,  some half baked ideas
        # for i,opt in enumerate(iterArgs):
        #   l = opt
        #   for ii, oopt in enumerate(l):
        #     if opt == '--':
        #       'switch to taking filenames only not arguments anymore'
        #     if opt.endswith( '=' ):
        #       n iterArgs.__next__()
        #       opts[oopt]=
        #     l.append( n   )
        #
        # print( opts )

        
    @classmethod
    def Cd(cls, path):
        import os
        os.chdir( path )
        return os.getcwd()
    
    @classproperty
    def ContextManager(cls):
        import contextlib
        return contextlib.contextmanager
    
    
    @classmethod
    def CropListUpToFirstNewline( cls, ls):
        return Utils.Funcs.CropListUpToFirstNewline( ls )
        """
        return True if newline was found else False
        
        modifies list in place
        if first newline found is at end of last item, list will be unmodified
        even though we return True
        """
        if len(ls)==0:
            return False
        else: #list ls has length
            ## loop through all except the last
            for i in range(  len(ls) - 1  ):
                item = ls[i]
                if isinstance( item, str ):
                    if '\n' in item:
                        del ls[i+1:] ## delete all indexes higher than this
                        del item
                        break
                del item
            ## at this point, the first occurance of '\n'
            ## would be at end of list, if it exists at all,
            ## since any list entries after first occurance were removed

            last = ls[-1]
            if not isinstance( last, str ):
                ""  #not a string, so do nothing
                return False
            else:
                foundInLast=False
                gather=''
                for c in last:
                    if c!='\n':
                        gather=gather + c
                    else:
                        foundInLast=True
                if not foundInLast:
                    ""  # doesn't have newline, so do nothing
                    return False
                else:
                    ls[-1] = gather
                    return True
        ## newline not found at all
        return False    
    
    
    @classmethod
    def Dir(cls, obj, includePreAndPostDoubleUnderscored=False ):
        d = dir(obj)
        if includePreAndPostDoubleUnderscored==False:
            l = []
            for i in d:
                if not i.startswith('__'):
                    if not i.endswith('__'):
                        l.append( i )
            return l
        else:
            return d


    @classmethod
    def DirToObj(cls, obj, *args, **kwargs ):
        d = cls.Dir( obj, *args, **kwargs )
        newObj = Object()
        for k in d:
            v = getattr( obj, k )
            setattr( newObj, k, v )
        return newObj

    @classmethod
    def DictCopyExclusive( cls, dictToCopy, keysToExcludeIterable ):
        print( keysToExcludeIterable )
        try:
            copy = dictToCopy.copy()
            for key in keysToExcludeIterable:
                if key in copy:
                    del copy[key]
        except Exception as e:
            raise type(e)(
                str(e)
                + "      obj is not iterable (or is accidentally a str or bytes, and may need to be split to list)"
            )
        return copy
            
                               
                               
    @classmethod
    def DictOfDefaultsOntoObj( cls,
            obj, defaultsDict=None, attrDict=None, attrOnlySelfDict=None,
            fallbacks=False,
            replaceDictNones=True, ## allow replacing existing keys if they are None
            insertNewNones=True, ## allow inserting new attr even if they are None
            filterInput=None,
            filterOutput=None,
            modifyOriginal=True,
        ):
        ## *** todo - could add option to store
        ## entriesToApply on an obj attr
        
        
        
        if attrDict==None:
            attrDict={}
        
        if filterInput is not None:
            attrDictFiltered = attrDict.copy()
            for key in tuple( attrDictFiltered.keys() ):
                if not key in filterInput:
                    del attrDictFiltered[key]
        else:
            attrDictFiltered = attrDict
                
        
        
        simpleCase = (
            defaultsDict==None and
            replaceDictNones and
            insertNewNones
        ) 
                
        
        if simpleCase:
            for k,v in attrDictFiltered.items():
                setattr( obj, k, v )
        elif defaultsDict==None:
            for k,v in attrDictFiltered.items():
                if insertNewNones:
                    setattr( obj, k, v )
        ## this one will modify input dict, 
        else:
            #print( fallbacks )
            entriesToApply = cls.DictOfDefaultsOntoDict(
                defaultsDict,
                attrDictFiltered,
                replaceDictNones=replaceDictNones,
                insertNewNones=insertNewNones,
                fallbacks=fallbacks,
                modifyOriginal=modifyOriginal,
            )
            
            if filterOutput is not None:
                for key in tuple( entriesToApply.keys) :
                    if not key in filterOutput:
                        del entriesToApply[key] 
            
            if insertNewNones==True:
                for k,v in entriesToApply.items(): 
                        setattr( obj, k, v )            
            else:
                for k,v in entriesToApply.items():
                    if v is not None:
                        setattr( obj, k, v )            
            #for k in specifiedDict: 
            #    if k in entriesToApply:
            #        setattr( obj, k, entriesToApply[k] )
            #    elif k in destDict:
            #        v = destDict[k]
            #        if insertNewNones==True:
            #            setattr( obj, k, v )
            #        elif v!=None:
            #            setattr( obj, k, v )
                
            ## also need to handle entries that were already in
            ## destDict but were not on obj
        return obj
    
    @classmethod
    def DictOfDefaultsOntoDict(cls,
        defaultsDict, destDict,
        fallbacks=False,  ## don't usee values in default dict directly,
                          ## instead treat them as lists and take first non none
        replaceDictNones=True, ## allow replacing existing keys if they are None
        insertNewNones=True, ## allow inserting new attr even if they are None
        returnIncludingAlreadyExisting=True,
        filterInput=None,
        modifyOriginal=True,
        returnDestDict=False,
        ):
        
        if not modifyOriginal:
            destDict = destDict.copy()
        
        entriesToApply = { }
        entriesAlreadyExisting = { }
        
        for defaultEntryName, defaultEntryValue in defaultsDict.items():
            hasExistingKey = defaultEntryName in destDict
            
            #print( f"defaultEntryName is : {defaultEntryName}" )
            #print( f"replaceDictNones is : {replaceDictNones}" )
            ## check to see if we are allowed to
            ## insert a key and have one to insert 
            mightInsertKey=False
            
            if hasExistingKey:
                destDictAtDefaultEntryName = destDict[defaultEntryName]
                
                ## we need to keep track of which entries we didn't insert only because
                ## they were already there AND, optionally, non None
                if destDictAtDefaultEntryName!=None:
                    entriesAlreadyExisting[defaultEntryName] = destDictAtDefaultEntryName
                elif replaceDictNones==True:
                    mightInsertKey=True
                    if returnIncludingAlreadyExisting==True:
                        entriesAlreadyExisting[defaultEntryName]=None
                        
 
            if not hasExistingKey or mightInsertKey:
                ## if use of fallbacks has been requested, iterate to find
                if fallbacks==True:
                    #print( f"defaultEntryName is : {defaultEntryName}" )
                    #print( f"defaultEntryValue is : {defaultEntryValue}" )
                    destValue = cls.GetFirstNonNoneElseReturnNone(defaultEntryValue)
                    #print( f"destValue is : {destValue}" )
                else:
                    destValue = defaultEntryValue
                if destValue!=None or insertNewNones==True: 
                    entriesToApply[defaultEntryName]=destValue



        if filterInput is not None:
            keys = entriesToApply.keys()            
            for k in keys:
                if not k in filterInput:
                    del entriesToApply[key]
                    
        for k,v in entriesToApply.items():
            if filterInput is not None:
                if not k in filterInput:
                    continue
            destDict[ k ] = v
        
        #print( fallbacks )
        #print( defaultsDict )
        
        
        if returnDestDict:
            return destDict
        else:
            if returnIncludingAlreadyExisting:
                returnDict = { **entriesAlreadyExisting, **entriesToApply }
            else:
                returnDict = entriesToApply
                    
            return returnDict


    @classmethod
    def DictOfDefaultsOntoDictWithBackup(cls, *args, **kwargs):
        defaultsDict = args[0]  ## first required arg of func we'll call
            #kwargs.get( 'defaultsDict', {} )
        #if defaultsDict is not {}:
        backup = defaultsDict.copy()
        #else:
        #    backup = None
        return backup, cls.DictOfDefaultsOntoDict( *args, **kwargs )

    @classmethod
    def EnumArgs(cls):
        import sys
        return enumerate( sys.argv[1:] )
    
    @classmethod
    def EnvGet(cls, varName=None, splitStr=None, index=None ):
        e = cls.Envs
        if varName is None:
            return e
        else:
            ev = e[varName]
            if splitStr is None:
                return ev
            else:
                evs = ev.split(splitStr)
                if index is None:
                    return evs
                else: 
                    evsi = evs[index]
                    return evsi
    
    @classmethod
    def Eval(cls, codeToExec, codeToEval=None, g=None, l=None,):
        retVal=None
        import inspect
        frame = inspect.currentframe().f_back
        try:
            if l is None:
                l = frame.f_locals
            if g is None:
                g = frame.f_globals
            if codeToExec is not None:
                exec( codeToExec, g, l )
            if codeToEval is not None:
                retVal = eval( codeToEval, g, l )
        finally:
            del frame
        return retVal

    @classmethod
    def Exit(cls, *args, **kwargs):
        import sys
        sys.exit(*args, **kwargs)          

    @classmethod
    def ExtendBuiltinClass(cls, clsToExtend, callFunc, callName=None ):
        from .submodules import forbiddenfruit
        if callName == None:
            callName = callFunc.__name__
        return forbiddenfruit.curse( clsToExtend, callName, callFunc )
    
    @classmethod
    def FileRead(cls, filePath ):
        fh = open( filePath )
        contents=txt = fh.read()
        fh.close()
        return contents
    
              
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
    def Format( *args, **kwargs ):
        args=list(args)
        hasError=False
        if args!=None:
            if len(args)>0:
                string0=args.pop(0)
                return string0.format( *args, **kwargs )
            else:
                hasError=True
        else:
            hasError=True
        if hasError==True:
            raise TypeError( "string required as first argument to this Format function" )

    @staticmethod
    def FormatV( string0, args=None, kwargs=None ):
        if args==None:
            args=[]
        if kwargs==None:
            kwargs={}
        #print(kwargs)
        return string0.format( *args, **kwargs )
    
    @classproperty
    def Frame(cls):
        import inspect
        return inspect.currentframe
    
    @classmethod
    def FromFrame(cls, frame, kind=None):
        """
        Use this via
        Easy.FromFrame( Easy.Mods.inspace.currentframe() )
          pass inspect.getframe() to this function to return
          info gathered from frame
          
        It can only find functions in the flib functionLibrary
          they can be added with the decorator
          Easy.Flib.Add
          
        related into
        #frame.f_code.co_name
        # func.__name__  
        #freevars=func.__code__.co_freevars
        #closure=func.__closure
          
        """
        if kind is None or kind=='func' or kind=='function':
            n = frame.f_code.co_name
            f = cls.Flib.get(n)
            return f #, n
    
    @classmethod
    def GetCwd( cls ):
        import os
        return os.getcwd()

    @classmethod
    def GetFirstNonNoneElseReturnNone( cls, fallbacks ):
        for fb in fallbacks:
            if fb!=None:
                return fb
        return None
    
        ## *** todo later
        ## could check for utility class for other keyword fallbacks
        ## in case
        ## until then, fallbacks must be iterable        
        ## and/or check for iterable
        ##        try:
        ##        iterator = iter(fallbacks)
        ##    except TypeError:
        ##        ## later, include option to use alternate keys as fallbacks
        ##        raise TypeError('Fallbacks must be iterable.' )
        ##    else: # fallbacks is iterable
        ##        attrValue = None
             
    @classmethod          
    def GetHost(cls):
        import socket
        host = socket.gethostname()    

    @classmethod
    def GetUser(cls):
        import getpass
        getpass.getuser()


    @classmethod
    def GetPrompt(cls):
        """Get a generic prompt, especially useful for xonsh
        """
        host = socket.gethostname()
        user = getpass.getuser()
        pr = ''
        pr+= user
        pr+= '@'
        pr+= host
        pr+= ' >> '
        pr+= os.getcwd()
        pr+= '> '
        return pr
    
         
    @staticmethod
    def GetRoutinesFromObj(sourceObj):
        import inspect
        l=inspect.getmembers( sourceObj, inspect.isroutine)
        result=[]
        for iname, i in l:
            i.__name__=iname
            #print( i.__name__ )
            result.append (i)
        return result    

    @classmethod
    def Glob(cls, *args, **kwargs):
        import glob
        return glob.glob( *args, **kwargs )    

    @classproperty
    def Ic(cls):
        return ic ## func in this module root namespace    

    @staticmethod
    def Import(modname, byFilePath="unimplemented"):
        import importlib
        return importlib.import_module( modname )
        
    @classmethod
    def ImportFile( cls, path, asName= None, relativeToScript = "unimplemented" ):
        import importlib, os
        fileName=path.split(os.sep)[-1]
        if asName== None:
            asName = fileName[:-3]
        spec = importlib.util.spec_from_file_location( asName, path )
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m


    @classmethod
    def JoinDir(cls, *args, ext=''):
        """
        Joins all args as path components and optionally adds  ext  on the end
        """
        import os
        return os.path.join( *args ) + ext

    @classmethod
    def JoinDirFileExt(cls, dir, fbname, ext ): #cleanTrailingSlashes=False):
        import os
        fname = fbname + ext
        return os.path.join( dir, fname )  #*[dir, fname]
        

    @classmethod
    def Ls(cls, *args):
        import os
        return os.listdir( *args )        

    @classmethod
    def LsAbs(cls, path):
        import os
        if False:
            oldDir = os.getcwd()
            os.chdir( path )
            l = os.listdir( )
            ## careful, os.path.abspath is relative to cwd, not path
            ## this only works because we chdir
            lAbs = [ os.path.abspath(i) for i in l ] 
            os.chdir( oldDir )
        else:
            l = os.listdir( path )
            lAbs = [ os.path.join( path, e ) for e in l ]     
        return lAbs

    @classmethod
    def Namespace(cls,*args,**kwargs):
            import types
            return types.SimpleNamespace(*args,**kwargs)
        
    @classmethod
    def NamespaceComplex(cls,*args,**kwargs):
            import argparse
            return argparse.Namespace(*args,**kwargs)
        
        
        

    @classproperty
    def Now(cls):
        return cls.NowUtc
    @classmethod
    def NowUtc(cls):
        import datetime
        return datetime.datetime.utcnow()
        
    @classmethod
    def NowLocal(cls):
        import datetime
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
    def NowLocalStr(cls, fmt=None, style=None,alphanum=False):
        if fmt is None:
            if alphanum:
                fmt = "y%Ym%md%dh%Hn%Ms%SAsLocalTime"
            else:
                fmt = "%Y-%m-%dT%H%M%S%z"
            if style==None:
                'pass'
            else:
                'pass'
        return cls.NowLocal().strftime(fmt)[:22]  ## todo  fix this

    @classproperty
    def ODict(cls):
        import collections
        return collections.OrderedDict


    @classproperty
    def OntoDict(cls):
        return cls.DictOfDefaultsOntoDict
    
    @classproperty
    def OntoDictWithBackup(cls):
        return cls.DictOfDefaultsOntoDictWithBackup
    
    @classproperty
    def OntoObj(cls):
        return cls.DictOfDefaultsOntoObj
    
    @classmethod
    def PipInstall( cls, *args,  **kwargs ):
        import subprocess, sys
        pkgList = []
        for arg in args:
            pkgList.append( arg )
        packages = ' '.join(pkgList)
        
        #if action=='install'
        for arg in args:
            subprocess.call(
                [
                    sys.executable,
                    "-m", "pip", "install",
                    "-U", "--user",
                    packages,
                ]
            )

    @classmethod
    def Prints(cls, *argsS, **kwargs):
        for args in argsS:
            for arg in args:
                print( arg, **kwargs )

        
    @classmethod
    def PrintFile(cls, *args, **kwargs ):
        args = list(args)
        with open( args[0], 'r' ) as fh:
            txt = fh.read() 
        args[0] = txt
        print( *args, **kwargs )

        
        
    @classmethod
    def PrintLoop(cls, *args,
            count=1, sleep=0, endAll=None,
            header=None, footer=None,
            **kwargs,
            ):
        if sleep>0:
            import time
            sleepFunc= time.sleep
        
        def tmpPrint( argsAndKwargsTuple ):
            #print( f"argsAndKwargsTuple is:  {argsAndKwargsTuple}, {type(argsAndKwargsTuple)}" )
            if argsAndKwargsTuple is not None:
                tmpArgs, tmpKwargs = argsAndKwargsTuple
                #print( f"tmpArgs is:  {tmpArgs}, {type(tmpArgs)}" )
                assert isinstance( tmpArgs, tuple )
                assert isinstance( tmpKwargs, dict )
                #print( repr(tmpArgs) )
                #print( repr(tmpKwargs) )
                if len(tmpKwargs) > 0:
                    print( *tmpArgs, **tmpKwargs )
                else:
                    print( *tmpArgs )
        
        if header is not None:
            tmpPrint(header)
        
        for i in range(count):
            print( *args, **kwargs )
            if sleep>0:
                sleepFunc( sleep )
        
        if endAll is not None:
            print( endAll, end="" )
        
        if footer is not None:
            tmpPrint(footer)
    
    
    @classmethod
    def PrintTail( cls, *args, **kwargs ):
        """
        Print the last n lines of each argument.
        
        Can pass
        """
        tailsep = kwargs.get( 'tailsep', '\n\n' )
        asList = kwargs.get( 'asList', None )        

        kwargs['asList']=True ## set option for call to cls.Tail
        tails = cls.Tail( *args, **kwargs )
        

        ## prep kwargs for print
        kwargs.pop( 'tailsep', None )
        kwargs.pop( 'asList', None )
        kwargs.pop( 'n' )
        
        ##print them
        for i,t in enumerate(tails):
            if tailsep!=None:
                if i>0:
                    print( tailsep, end='' )
            print( t, **kwargs )
                
        if asList:
            return tails
        else:
            s = tailsep.join( tails )
            return s
            
    @classmethod
    def PrintTraceback(cls):
        import traceback
        print( traceback.format_exc() )



    @classmethod
    def PrintVar(cls, var, msg=None, showValue=True, showRepr=True, showType=True, g=None, l=None,):
        retVal=None
        import inspect
        frame = inspect.currentframe().f_back
        try:
            if l is None:
                l = frame.f_locals
            if g is None:
                g = frame.f_globals
            if msg is not None:
                print( msg )
            if True:
                val = eval( var, g, l )
                str = ''
                str+=f'{var}'
                if showValue:
                    str+=' '
                    str+=f'is: {val}'
                if showRepr:
                    str+=f'  '
                    str+=f'repr: {repr(val)}'
                if showType:
                    str+=f'  '
                    str+=f'type: {type(val)}'
                print( str ) 
        finally:
            del frame
        
    @classmethod
    def PrintVars(cls, vars, msg=None, showValue=True, showRepr=True, showType=True, g=None, l=None,):
        retVal=None
        import inspect
        frame = inspect.currentframe().f_back
        try:
            if l is None:
                l = frame.f_locals
            if g is None:
                g = frame.f_globals
            if msg is not None:
                print( msg )
            for var in vars:
                val = eval( var, g, l )
                str = ''
                str+=f'{var}'
                if showValue:
                    str+=' '
                    str+=f'is: {val}'
                if showRepr:
                    str+=f'  '
                    str+=f'repr: {repr(val)}'
                if showType:
                    str+=f'  '
                    str+=f'type: {type(val)}'
                print( str ) 
        finally:
            del frame
        
    @classmethod
    def PrintWithFormat( cls, string0, *args, **kwargs ):
        """
        Print and formats a single given string argument.
        Other arguments will be passed to format function.
        """
        s = cls.Format( string0, *args,**kwargs)
        print(s)
        return s
    
    @classmethod
    def PrintWithFormatV( cls, string0, args=None, kwargs=None, sep=' ', end='\n' ):
        s = cls.FormatV(string0,  args, kwargs )
        print(s, sep=sep, end=end )
        return s
              
    @staticmethod
    def ReloadModule( targetMod=None, name=None, fallbackMod=None):
        from . import EasyConf
        import importlib
        if fallbackMod==None:
            fallbackMod=SelfMod
        if targetMod is None and name is None:
            defaultModToReturn=fallbackMod
        else:
            defaulModToReturn=None
        print( EasyConf.ReloadWarning )
        try:
            if targetMod is None:
                if name is None:
                    name=__name__
                targetMod = __import__( name )
            ## At this point, targetMod, explicit,
            ## or foundByName, or purposefully None
            defaultModToReturn=targetMod
            mod = importlib.reload( targetMod )
            return mod
        except:
            cls.PrintTraceback()
            return defaultModToReturn
    
    @classmethod
    def Rreplace(cls, inputString, old, new, maxCount=-1):
        if maxCount >= 0:
            li = inputString.rsplit(old, maxCount)
        else:
            li = inputString.rsplit(old)
        return new.join(li)
    
    @classmethod
    def ReplaceEnd(cls, inputString, old, new):
        if not inputString.endswith( old ):
            return inputString
        else:
            return cls.Rreplace( inputString, old, new, 1 )

    @classproperty
    def See(cls):
        return see  ## function is this modules root namespace

    @classmethod
    def Sleep(cls, *args, **kwargs ):
        import time
        return time.sleep( *args, **kwargs )
    
    @classmethod
    def TmpDir(cls, *args, **kwargs):
        import tempfile
        return tempfile.mkdtemp( *args, **kwargs )
    
    @classmethod
    def TmpDirContext(cls, *args, **kwargs):
        """
        warning, this offers no way to set delete=False
        can cause a weird recursion depth problem on sys exit
        when it can't delete the file
        and exceptions can trigger more exceptions
        """
        import tempfile
        return tempfile.TemporaryDirectory( *args, **kwargs )
    
    @classmethod
    def TmpFile(cls, *args, **kwargs):
        import tempfile
        return tempfile.mkstemp( *args, **kwargs )
    
    @classmethod
    def TmpFileContext(cls, *args, **kwargs):
        import tempfile
        return tempfile.NamedTemporaryFile( *args, **kwargs )
    
    @classmethod
    def Traceback(cls):
        import traceback
        return traceback.format_exc()

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
        
    @classmethod
    def TzOff(cls):
        import datetime
        now=datetime.datetime.now()
        utcnow=datetime.datetime.utcnow()
        offset=now - utcnow
        return offset

    @classmethod
    def TzLocal(cls):
        import datetime
        return datetime.timezone( cls.TzOff() )        
 
    @classmethod
    def UniqueIntHuge(cls):
        import time, uuid
        id = uuid.uuid4().int \
            + ( 1+ 2**128*uuid.uuid1().int ) \
            + (2**256)*time.process_time_ns()
    


    
    ## This function is GREAT for flattening nested sibling for-loops
    @classmethod
    def YieldFlat( cls, *args ):
      #print( args )
      #exit()
      for id, arg in enumerate(args):
        for item in arg:
          yield ( item, id )



UtilsModLoadingIsComplete=True
'''
decorator todo:
def export(func):
    mod = sys.modules[func.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(func.__name__)
    else:
        mod.__all__ = [func.__name__]
    return func
'''