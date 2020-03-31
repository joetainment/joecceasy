#!/usr/bin/env python3
from joecceasy import Easy; exec( Easy.Code ); exit() #%exit  
## the above line needs the magic, at its end: #%exit

## Easy.Code is the code of the running script,
## translatesd so that lines with magic tokens,
## write out automated python source code,
## which is executed.

## The call below will run the system command "dir"
#%callq dir

## result is available in local tmpResult var:
print( type(tmpResult) )
Easy.PrintTail(  'result: ' + tmpResult.stdout )

