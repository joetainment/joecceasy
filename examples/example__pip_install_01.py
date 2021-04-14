#!/usr/bin/python3
from joecceasy import Easy

pkg="isodate"  ## note that this testing script
               ## assumes pkg name is same as mod name,
               ## like "isodate" example.
               ## The test will fail otherwise,
               ## but Easy.PipInstall feature can be used without
               ## matching names as long as care is taken to use the 
               ## correct different pkg and mod names 

try:
    pkgMod = Easy.Mods[pkg]
except:
    print( f""" {pkg} package not found, attempting pip install..."""  )
    Easy.PipInstall( pkg )
    print( f""" {pkg} package installed """ )
    pkgMod = Easy.Mods[pkg]


print( f"dir function used on pkg {pkg} shows:")
print( dir(pkgMod) )

Easy.Input( 'press enter to exit or wait 5 sec for timeout', 5, warn=0 )