## this script doesn't use discover since complex logic
## may decide how to run tests!

import datetime, os, platform, subprocess, sys, time

scriptAbsPath = os.path.abspath(__file__)
scriptDir = os.path.dirname(scriptAbsPath)
os.chdir(scriptDir)

exeAbsPath = sys.executable

pyExt='.py'
testPrefix='test__'

stdout, stderr = None,None
outputFh=None

#def msg(*args,**kwargs):
#  print(*args,**kwargs)
def msg( argOutputFh, *args, **kwargs):
  if not argOutputFh is None:
    print( *args, file=argOutputFh, **kwargs )
    print( *args, **kwargs )
    argOutputFh.flush()
  else:
    print( *args, **kwargs )

if '--output-to-delme-file' in sys.argv:
  doOutput=True
  outputFilePath = "gitignore--unittests-results-deleteme.txt"
  outputFh = open(outputFilePath, 'w').close()
  outputFh = open(outputFilePath, 'a' )
  stdout = outputFh
  stderr = outputFh
  #sys.stdout=

"""
subprocess.run(
        [ 'python', '-m', 'unittest',
          'discover', '-s', '.', '-p', 'test__*.py',
        ], stdout=stdout, stderr=stderr
)
"""

msg( outputFh, f'######## joecceasy python module unittests ########' )
msg( outputFh, f'sys.version: {sys.version}' )
msg( outputFh, f'sys.version_info: {sys.version_info}' )
msg( outputFh, f'os.name: {os.name}')
msg( outputFh, f'platform.system():{platform.system()}' )
msg( outputFh, f'platform.release():{platform.system()}' )
msg( outputFh, f'platform.platform():{platform.platform()}' )
msg( outputFh, f'platform.processor():{platform.processor()}' )
msg( outputFh, f'#### started at: {datetime.datetime.now()} ####')

for steproot, dirs, files in os.walk('.'):
  for file in files:
    isTest = file.lower().startswith(testPrefix)
    isPy = file.lower().endswith(pyExt)
    if isPy and isTest:
      msgAtStart = ( """############################\n"""
                  +"""#### Start test of python file: """
                  + file + "\n"
      )
      msgAtEnd = ( 
                  """#### End test of python file: """
                  + file + "\n"
                  +"""############################\n"""                  
      )
      print( file )
      msg(outputFh, msgAtStart, end='')
      subprocess.run(
        [ exeAbsPath, '-m', 'unittest', '-v', file ],
        stdout=stdout, stderr=stderr
      )
      msg(outputFh, msgAtEnd, end='' )
      msg(outputFh, "\n\n\n", end='' )
      
      
      
                  


    

msg( outputFh, f'#### ended at: {datetime.datetime.now()} ####')
if not outputFh is None:
  print( f'#### See output file: {outputFilePath}') 
  outputFh.close()
      