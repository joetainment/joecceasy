#!/usr/bin/env python3
from joecceasy import Easy; Easy.Init()

## Easy.ArgsE and Easy.Args give us easy access to our programs arguments,
## while conveniently not including zero sys.argv[0]
## (argument zero) this way we can easily process
## just the arguments given to this script.

for i, arg in Easy.ArgsE:
    print( f"arg at index {i}  (at sys.argv index {i+1}) : {arg}" )


## Same as the function call, Easy.EnumArgs()
#for i, arg in Easy.EnumArgs():
#    print( f"arg at index {i}: in sys index {i+1} : {arg}" )

## or, if we didn't want to bother enumerating them:
#for arg in Easy.Args:
#    print( f"Easy.Args contains: {arg}" )    

if Easy.ArgsCount < 1:
    print( Easy.TrimAndTab(r"""
        ###
        No arguments given.
        Please provide at least one argument.
        For example:
        By dragging and dropping a file onto this script.
    """))

