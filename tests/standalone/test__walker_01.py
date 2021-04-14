from joecceasy import *

try:
    pathToWalk = Easy.Args[0]
except IndexError:
    pathToWalk = ''

def main():
  pth = pathToWalk
  for entry in Easy.Walk( pth ):
    print( entry.__dict__ )
  print( ' \n ' )
  pathsAsIterable = [ pth ]
  for entry in Easy.WalkAnIter( pathsAsIterable ):
    print(entry.abs)
  print( ' \n ' )
  
  i = -1  
  for entry in Easy.Wwalk( pth ):
    i += 1
    isFileByPython = Easy.Mods.os.path.isfile(entry.abs)      
    print(
        'entry: ', entry.name,
        'f',entry.isFile, 'd', entry.isDir, 'l', entry.isLink,
        'fa', entry.isFileAt, 'da', entry.isDirAt,
        'pf', entry.isActFile, 'pd', entry.isActDir,
    )

  print( ' \n ' )

if __name__=='__main__':
    main()