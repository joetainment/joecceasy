from joecceasy import Easy

## Sultan is a nice way of running subprocess commands
##   use it via a normal instance of its class:
result = Easy.Sultan().cmd('ls','-la').run()

## or use it a via content manager
with Easy.Sultan.load() as sultan:
  ## cd will only persist for a single run does it as:  "cd;  ls;"
  result = s.cd('..').cmd('ls').run()
  Easy.Prints( r.stdout )
