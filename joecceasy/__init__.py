r"""
joecceasy python package __init__.py

Make Python Easy

This module, "joecceasy", is for prototyping,
early learning, and writing short scripts
without boiler plate code!
Remember, joecceasy is intentionally non-pythonic and 
does not follow "best practices", but it "gets it done quick".

## Recommended way of importing, without magic, is:
from joecceasy import Easy

## or...
from joecceasy import *
    ## using * will import Easy the same way, but it is
    ## but is less explicit, so it may be less obvious to others

## Recommended way of importing, with magic, is:
from joecceasy import *; exec(Easy.CodeQ); exit(); #%exit
  ## keep the #%exit in the line above


See the examples folder in the git source repository
for all sorts of examples of using joecceasy
and to see just how useful it can be.


Note, as a general rule, lowercase is only used for:
    - python builtins that have those standard names
        e.g. "os"
    - local vars in functions
    - module level vars, usually these aren't
        intended to be used by end users
    - plain functions in module scope or inside local scopes
        generally not thing intended to be called directly
        from outside the scope they are declared in
    - plain funcs inside other functions or methods
    - regular methods of classes
        not classmethods or static methods

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
  Easy.Args
      doesn't include arg zero, (which is usually script itself)
  Easy.ArgsE    enumerated arguments iterator!  e.g.
      for i,arg in Easy.ArgsE:
          print( f"arg number {i} is {arg}" )
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
    

  Easy.Magic can also be used instead, which provides of ton
      of extra "magic" functionality, such as populating
      the script with standard joecceasy vars.
      Using magic pretty much gives a joecceasy DSL.  ;)
      It exists specifically for writing useful One liners and
      other short scripts.

  Easy.Ic
    **warning do not use if var potentially contains untrusted code**
    prints the var's in code name and its value and type
    is inspired by icecream module, but is different
    e.g.
        x = "this will be printed"
        Easy.Ic( x )
    
    
  Easy.See
    **warning do not use if var potentially contains untrusted code**
    is similar to ic but takes an expression instead of code
    generally shows repr.   Anything that isn't a string will
    be expanded, so it works on lists of expressions etc
    will skip things that can't be expanded into strings
    e.g.
        x = 3
        Easy.See( 'x+3' )

  Easy.Fstring - For Using "late" F-Strings:
    e.g.
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
        are trimmed and unindented, to match first hash's indentation.
        They can end with backslashes too!
        Which really helps on for copy pasting literals on Windows
    ''')
    # e.g.
    Easy.TrimAndTab(r'''
        ###
        C:\Windows\
    ''')

  
"""
__version__ = "0.0.1rc1"
__author__ = 'Joseph Cameron Crawford (Joe)'
__credits__ = 'Joetainment, Joecc'

from . import Utils
from . import EasyMod
from .EasyMod import Easy


SelfMod = __import__(__name__)
SelfPak = SelfMod ## module is root init itself

Ez = Easy
ez = Easy

tt = Easy.TrimAndTab
TT = tt
Tt = tt

Tl = Easy.TrimLines
TL = Tl
tl = Tl

## make it easy to make exit work in scripts
exit = Easy.Exit
Exit = exit

__all__ = ['Easy']
    ## whatto import on: from joecceasy import *
    ##   don't use the others, because they can be
    ##   accessed through 'easy'
    # ,'SelfMod','SelfModule','SelfPak','SelfPackage']

