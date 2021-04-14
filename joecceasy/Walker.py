#### Note, this sorts by python string sorting
####   caps first, may not match gnu/linux ls command
####   dirs first, same
####    
####    isActFile matches os.path.isfile
####    isActDir matches os.path.isdir
####    isActLink matches os.path.islink
####
####    isFile isDir isLink are exclusive
####    isLink types won't also show as isFile or isDir,
####    unlike os.path.isfile and os.path.isdir
####
####    isFileAt will be true for both files and links to files
####    isDirAt  will be true for both dirs and links to dirs

import os

from . import Utils
#from .

#Self
path = os.path

pjoin = path.join
pabs = path.abspath
prel = path.relpath

classproperty = Utils.classproperty

#types = symlink_to_file symlink_to_noexist symlink_to_noaccess symlin

class Entry:
    def  __init__( self, *args, **kargs ):
        d = self.__dict__
        for k in kargs:
            d[k] = kargs[k]
    #def isDir(self):
    #def isDirLike(self):
    #    return
#    def isFile

class Walker:
  @classmethod
  def _yieldDirsAndFilesTogether(cls, walkDirs, walkFiles ):

      for  item, id  in  Utils.Funcs.YieldFlat( walkDirs, walkFiles ):
          yield  item, id
      #for iDir in walkDirs:
      #    yield ( iDir, True )
      #for iFile in walkFiles:
      #    yield ( iFile, True)
      
  @classmethod
  def WalkAnIter(cls, pathsIterable, useEmptyStrAsDot=True ):
      for pth in pathsIterable:
          for entry in cls.Walk( pth, useEmptyStrAsDot=useEmptyStrAsDot ):
            yield entry 

  @classmethod
  def Walk( cls, pth, useEmptyStrAsDot=True ):
    KargsAsObj = Utils.KargsAsObj
    
    if useEmptyStrAsDot and pth=='':
      pth='.'
    for walkStepRoot, walkDirs, walkFiles in os.walk( pth ):
      #print( f'walkStepRoot: {walkStepRoot}' )
      stepRoot=walkStepRoot
      if stepRoot==os.curdir:
          stepRoot= ""
      walkDirs.sort()
      walkFiles.sort()
    
      flatIter = cls._yieldDirsAndFilesTogether(walkDirs, walkFiles)
      for it, wasAsDirInFlatList in flatIter:
        wwd = os.getcwd()
        if stepRoot=='' or stepRoot==os.curdir: ## if it is '.' just a dot
            op = it    
        else:
            op = pjoin( stepRoot, it )

        isActFile= False
        isActDir=False
        isFile = False
        isDir = False
        isLink = False
        isFileAt = False
        isDirAt = False
        isBroken = False
        symDepth = 0
        #isFile, isDir, isLink=False,False,False ##defaults
        isActFile=path.isfile(op)
        isActDir=path.isdir(op)
        isLink = path.islink(op)        
        if isLink:
            if path.isdir(op):
                isDirAt=True
            elif path.isfile(op):
                isFileAt=True
            else:
                isBroken=True
            """            
          resMax=99
          resCount=0
          resDone=False
          res=os.path.abspath(op)
          while not resDone:
            resCount += 1
            if  resCount>resMax:
                isBroken=True
                break

            symDepth += 1
            targetDir=os.path.split(res)[0] ##head is [0]
            target=os.readlink(res)
            if not path.isabs(target):
                res=pjoin( targetDir, target )
            else: ## is abs
                res=target
            if not path.exists(res):
                isBroken=True
                break
            if path.islink(res):
                continue
            else: ## link resolved
                resDone=True
                if path.isfile(res):
                    isFileAt=True
                elif path.isdir(res):
                    isDirAt=True        
                else:
                    isBroken=True
            """
        ## At this point op can't be a link because we checked
        elif path.isdir(op):
            isDir=True
            isDirAt=True
        elif path.isfile(op):
            isFile=True
            isFileAt=True
        else:
            isBroken = True
            raise Exception('broken, should be one of file/dir/link')


        ap = pabs( op )
        rp = prel( op )
        real = path.realpath( op )


        #resolved = ''
        #type=''
        entry = KargsAsObj(
            orig= op,
            abs= ap,
            rel=rp,
            real= real, 
            wwd= wwd,

            isActFile = isActFile,
            isActDir = isActDir,
            isFile = isFile,
            isDir = isDir,
            isLink = isLink,
            isFileAt = isFileAt,
            isDirAt = isDirAt,
            isBroken = isBroken,
            symDepth = symDepth,
            name = it,
        )
        yield entry
        #entries.append( entry )
    #return entries


  @classproperty
  def walk( cls ):
    return cls.Walk
  @classproperty
  def wwalk( cls ):
    return cls.Walk

  def __init__(self, *args, **kargs):
      raise Exception(
          "This class should not ne instantiated, "
          +" it is for static only."
        )

## Setup vars for convenient access
walk = Walker.Walk
wwalk = Walker.walk
walkAnIter = Walker.WalkAnIter
