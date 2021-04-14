from joecceasy import Easy

## Create and run a Qtui app and have Python exit
## with Python returning the return code to the system/shell. 
## (See earlier examples for pre-requiisie understanding)
qtui = Easy.Qtui( title="Joecceasy Qtui Example" )
exitCode = qtui.execQapp()
Easy.Exit( exitCode )
