#!/usr/bin/env python3
from joecceasy import Easy

for i, arg in Easy.EnumArgs:
    print( f"arg at index {i}: in sys index {i+1} : {arg}" )

if Easy.ArgsCount < 1:
    print( Easy.TrimAndTab(r"""
        ###
        No arguments given.
        Please provide at least one argument.
        For example:
        By dragging and dropping a file onto this script.
    """))

