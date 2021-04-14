#!/usr/bin/env python3
from joecceasy import Easy;


def extension_method(self):
    return "This is an function to use as an extension method for str."
    
Easy.ExtendBuiltinClass(str, extension_method )  ## unimplemented as a decorator

print( "this is a string".extension_method() )


## name could be specified, as in:
# Easy.ExtendBuiltinClass(str, extension_method, extension_method.__name__ )
#   or
# Easy.ExtendBuiltinClass(str, extension_method, "some_name )
