'''
Configuration for the joecceasy module itself
'''   
from .Utils import Object  ## del this at end of this file

ReloadWarning = r"""
Easy-reloading the Easy module now. Hopefully you used  exec(Easy.ReloadStr)  or  Easy=Easy.Reload()  or something else similar.  Warning, this should only be used for simple tests. Reloading is inherently tricky and bug prone in Python. Reloading the interpreter is usually a better option.
"""[1:-1]

ReloadStr = r"""
import traceback
try:
  if 'Easy' in locals():
    from joecceasy import Easy
    Easy.Reload( )
except:
  print(  traceback.formatExc()  )

try:
  from joecceasy import Easy
  E = Easy
except:
  print(  traceback.formatExc()  )
"""

MagicConf = Object()
MagicConf.marks = Object()
MagicConf.marks.lit = ('#'+'%lit')
MagicConf.marks.call = ('#'+'%call')
MagicConf.marks.callQuiet = ('#'+'%callq')
MagicConf.marks.callNoLit = ('#'+'%nolit%%')
MagicConf.marks.exit = ('#'+'%exit')



## last lines of this file should remove any vars
## we don't want to be picked up in our conf
## such as imports etc
del Object  ## no more lines should come after these del lines