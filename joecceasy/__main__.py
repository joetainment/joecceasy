## because cSharp launcher has to pass it's rawCmd
## and I haven't figured out how to parse it in cSharp
##  to remove the variations of the executable, what would be argZero
## kinda sucks other uses of this module will need a dummy arg :(
## oh well.. fake it with a fake "run" subcommand
## python -m joecceasy run test.easy.py
##
## todo:
##   - make Mods an object that lazy loads modules on property access
##   - make modules not auto imported, or make them lazy too, and easily reloadable
##   - make assignment based printer, to avoid extra parens typing
##   - make assignment based printer, to avoid extra parens typing

import importlib, os, runpy, sys, traceback,math, random

import distutils.sysconfig as sysconfig
import os
import sys


from . import Utils

def get_standard_modules():
    found=[]

    std_lib = sysconfig.get_python_lib(standard_lib=True)

    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            prefix = top[len(std_lib)+1:]
            if prefix[:13] == 'site-packages':
                continue
            if nm == '__init__.py':
                found.append(  top[len(std_lib)+1:].replace(os.path.sep,'.')  )
            elif nm[-3:] == '.py':
                found.append( os.path.join(prefix, nm)[:-3].replace(os.path.sep,'.') )
            elif nm[-3:] == '.so' and top[-11:] == 'lib-dynload':
                found.append( nm[0:-3] )

    for builtin in sys.builtin_module_names:
        found.append( builtin )
        
    result = []
    for m in found:
        if '.' in m:
          continue
        if '_' in m:
          continue

        if 'site'==m:
          continue

        if 'antigravity'==m:
          continue
          
        if 'this'==m:
          continue
          
        #if 't' in m[:3]
        if True: ##'t' in m[2:3]:
            #print(m)
            if not m in result:  
                result.append(m)
          
    return result
    
modNames = get_standard_modules()

#print( *modNames, sep="\n")

Mods = Utils.Object()
ModsDict = {}
for n in modNames:  ## sys.builtin_module_names not enough
    try:
        im=importlib.import_module( n )
        setattr(Mods, n, im)
        ModsDict[n]=im
    except:
        ##just skip it, error will instead occur on use attempt
        'pass'


oldSysArgv = sys.argv.copy() # or list(sys.argv)
oldArg0=None  ## this will be the joecceasy/__main__.py
oldArg1=None  ## this will be the dummy command or the launcher path 
if len(sys.argv)>0:
    oldArg0 = sys.argv.pop(0)
    if len(sys.argv)>0:
        oldArg1 = sys.argv.pop(0)

if oldArg0==None or oldArg1==None or len(sys.argv)<1:
    not_enough_args_msg = (
        "\n"
        "FAILURE"
        "\n"
        "joecceasy module cannot run since sufficient arguments "
        "have not been provided."
        "\n"
        "Please provide at least one EasyPython file as "
        "an argument if using the launcher."
        "\n"
        "e.g. joecceasyLauncher yourscript.easy.py"
        "\n"
        "If using the module, provide the 'run' command and "
        "specify a script to run."
        "\n"
        "e.g. python -m joecceasy run yourscript.easy.py" 
    )
    print( not_enough_args_msg  )
    
    #print( f"sys.argv: {sys.argv}" )
    #print( f"oldArg0: {oldArg0}" )
    #print( f"oldArg1: {oldArg1}" )
    
    exit( )


#print( f"oldSysArgv: {oldSysArgv}" )



## get Easy
joecceasy = sys.modules[__package__] 
Easy = sys.modules[__package__].Easy
Easy.Inst



newGlobals={
        'joecceasy':joecceasy,
        'Easy': Easy,
        'Mods':Mods,
}

for k,v in ModsDict.items():
    newGlobals[k]=v

#print( f"newGlobals: {newGlobals}" )


#print( f"sys.argv before run is: {sys.argv}" )
runpy.run_path(
    sys.argv[0],
    init_globals=newGlobals,
    run_name="__main__",
)




#print( f"sys.argv: {sys.argv}" )
#print( f"package: {__package__}" )
#print( f"name: {__name__}" )


#for mod in sys.modules:
#  #print( mod )
#  'pass'



"""

print( sys.argv )
print( sys.argv[0] )
print( sys.argv[0] )
print( sys.argv )
"""




"""

## adjust cwd with given script's path
# may need to change and work into init call below

## initialize it and get it
Easy = joecceasy.Easy  #.Init( options )


## could handle args here and setup sys.argv manually
## runpy will also update it.

print(f"Easy.Args: {Easy.Args}" )
#sys.argv[0]
#argsForRun=Easy.Args




#sys.argv.clear()
#sys.argv.extend( Easy.Args )  ## sys.argv[0] get replaced anyway on run


#print(f"arg0NoQ: {arg0NoQ}" )
## do stuff for new sys args



#import ..joecceasy
#    Easy.CallInteractive( "notepad.exe" )

## __init__.py will have already run
#import .

#importlib.import_module( ".." + __package__ )
#Easy.Inst

#from .. import __package__
#print( joecceasy )
#print( 'main' )
#print( sys.argv )
#print( Easy.Args )

"""