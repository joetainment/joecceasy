#!/usr/bin/env python3
from joecceasy import Easy; exec( Easy.Magic ); exit() #%exit  
## the above line needs the magic, at its end: #%exit

#%call echo Starting for loop...

## The magic code will work in indented python code blocks
## as long as the block isn't otherwise empty
## which is why we include a line with only the string 'pass'
for i in 0,1,2:
    ## The call below will run the system command "dir"
    #%call echo This is a magic call inside a for loop.
    #%call echo This is iteration index #%i%#
    'pass' ## the "if" block needs a non-comment line
           ## just a standard python rule

#%call echo For loop is complete.