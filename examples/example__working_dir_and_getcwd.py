#!/usr/bin/env python3
from joecceasy import Easy; Easy.Init();

## current working dir is auto changed
## when using typical initialization
## of Easy class instance.
## e.g. when accessing Easy.Magic
## or calling Easy.Init()
##
## So here, current working dir is changed,
## but... other dirs are kept track of!  Yey!
print( "current dir is:" )
print( Easy.Cwd ) ## same as os.getcwd()
print( "but also remembers original working dir:" )
print( Easy.OrigWorkDir )
print( "script dir is available even after changing directory:" )
#Easy.Chdir( )
print( Easy.ScriptDir )
print( "If script was started when working dir was script's dir, the above 3 will all be the same." )

