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
    r = Easy.PrintWithFormatV( exampleToFormat, kargs=locals(), end='\n\n\n' )
    # we don't have to print the results
    unprinted = Easy.Format( exampleToFormat, number=4 )
    # or
    substitutions={ 'number': 5}
    unprinted = Easy.FormatV( exampleToFormat, kargs=substitutions )
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

from .Easy import Easy
from . import Easy as EasyMod
SelfMod = __import__(__name__)
SelfPak = SelfMod ## module is root init itself


## whatto import on: from joecceasy import *
##   don't use the others, because they can be
##   accessed through 'easy'
# ,'SelfMod','SelfModule','SelfPak','SelfPackage']

__all__ = ['Easy']
