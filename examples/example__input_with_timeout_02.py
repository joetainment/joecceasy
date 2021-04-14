import os, sys, traceback, subprocess

from joecceasy import Easy

timeout=5
print( f'About to get input (with timeout)...' )
print( f'Note that default input will be received after {timeout} seconds.' )
got = Easy.Input(
        f'Input - hurry, before {timeout} second timeout!:',
        timeout=timeout, default=None
)
print(
  f'received input was: {got}\n{repr(got)}    {type(got)}'
)