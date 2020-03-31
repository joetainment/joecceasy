#!/usr/bin/env python3
from joecceasy import Easy; exec( Easy.Code ) ; exit() #%exit

## current working dir is auto changed!
## but other dirs are kept track of
print( "current dir is:" )
print( Easy.Cwd ) ## same as os.getcwd()
print( "but also remembers original working dir:" )
print( Easy.OrigWorkDir )
print( "but also remembers original working dir:" )
print( Easy.ScriptDir )
print( "If script was started when working dir was script's dir, the above 3 will all be the same." )

