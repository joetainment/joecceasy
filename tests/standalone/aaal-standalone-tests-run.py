import os, subprocess, sys, time

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
    argOutputFh.flush()
  else:
    print( *args, **kwargs )

if '--output-to-delme-file' in sys.argv:
  doOutput=True
  outputFilePath = "gitignore--test-results-deleteme.txt"

  outputFh = open(outputFilePath, 'w').close()
  outputFh = open(outputFilePath, 'a' )
  stdout = outputFh
  stderr = outputFh
  #sys.stdout=


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
      subprocess.run( [exeAbsPath, file], stdout=stdout, stderr=stderr )
      msg(outputFh, msgAtEnd, end='' )
      msg(outputFh, "\n\n\n", end='' )
      
      
      
                  

if not outputFh is None:
  outputFh.close()


    
      
      