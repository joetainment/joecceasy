from joecceasy import Easy

## make a qtui that uses a timer based callback
## to run code on update
## using function as lambda inline
qtui = Easy.Qtui( title="JoecceasyQtuiExample",
    updateInterval=1000,
    callbacks={
        'update' :  lambda self:  self.print(
            f"Update at time: {Easy.Mods.time.time()}"
        ),
    },
    showInput=False,
    autoExpandOutput=True, 
)
exitCode = qtui.execQapp()
Easy.Exit( exitCode )
