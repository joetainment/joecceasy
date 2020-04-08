#!/usr/bin/env python3
from joecceasy import Easy; exec( Easy.Magic ); exit() #%exit  
## the above line needs the magic, at its end: #%exit

## The call below will run the system command "dir"
## but won't automatically print the output
## since it is using the quiet version: #%callq

#%callq echo This is a quiet call.


## result is available in local tmpResult var
## ...thus...
## If we want to print it ourselves, we can use a regular print
## and print the call result's stdout
print(  'result: ' + tmpReturned.stdout )

## the result is of type:
## subprocess.CompletedProcess
## (from the subprocess module)