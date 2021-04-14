from joecceasy import Easy



#self.print( "command is:" + cmd )

## ui will be frozen whle running command
## in future should try doing subprocess in a separate thread
import subprocess
import sys


import subprocess
from threading import Thread 
import time
import queue

import subprocess
from threading import Thread 
import time
import collections
import io

class Duck():
    "pass"

class Tubprocess():
    OutErrTuple = collections.namedtuple('OutErrTuple',['out','err'])
    
    @staticmethod
    def moveFromQToList( q, l ):
            while True:
                try:
                    gotChar = q.get_nowait()
                    l.append( gotChar ) 
                except queue.Empty:
                    break
                
    #def __next__(self):
    #    raise StopIteration
    
    
    def __init__(self,
                cmdAndArgsAsIter=None, sleep=0.01,
                shell=False, shellCmdJoin=True,
                errToOut=False,
                ## old extra args:   autoRun=False
            ):               
        self.cmdAndArgsAsIter = cmdAndArgsAsIter
        self.sleep = sleep                 
        
        self.shell=shell
        self.shellCmdJoin=shellCmdJoin
        
        self.errToOut = errToOut
                 
        self.qOut = queue.Queue()
        self.qErr = queue.Queue()
        
        self.outList = []
        self.errList = []
        
        self.errStrLast=''
        self.outStrLast=''
        self.outListLastLen=0
        self.errListLastLen=0
        
        self.threads =  Duck()

        self.reader = self.getReaderFunc()
        
        self.iterObj=None
        
        self.retVal=None
        self.isRunInProgress=False
        self.isIterInProgress=False
        self.isAlreadyRan=False
        
        #if autoRun==True:
        #    assert self.cmdAndArgsAsIter is not None
        #    self.run()

    @property
    def outStr(self):
        outList=self.outList
        if self.outListLastLen <= len(outList):
            self.outStrLast = ''.join(outList)
        
        return self.outStrLast
    
    @property
    def errStr(self):
        errList=self.errList
        if self.errListLastLen <= len(errList):
            self.errStrLast = ''.join(errList)
        
        return self.errStrLast


    def next(self):
        if self.iterObj==None:
            self.iterObj=self.__iterRun()
        return next( self.iterObj )
        
    def __iter__(self):
        ## can only iterate once!
        if self.iterObj==None:
            self.iterObj=self.__iterRun()
        for i in self.iterObj:
            yield i        
        
    def getReaderFunc(self):
        if  hasattr( self, 'reader' ):
            return self.reader
        
        ## this func should use only local state
        ## so it can be threaded
        def reader(f,q):
            #optTime=0.01
            #sleepTime=0.3
            
            #lastTime = time.time_ns()
            doBreak = False
            while True:
                try:
                    gotChar=f.read(1)
                except ValueError as err:
                    break
                if gotChar:
                    q.put(gotChar)
                else:
                    doBreak =  True
                if doBreak:
                    break
        return reader
    
    def makeThread(self):
        "pass"
    
    def joinProcAndThreads(self):
        self.retVal = self.ps.wait()
        threads=self.threads
        threads.outReader.join()
        threads.errReader.join()
        self.isRunInProgress=False
    
    def __runProcAndThreads(self):
        assert self.isAlreadyRan==False
        assert self.isRunInProgress == False
        self.isAlreadyRan=True
        self.isRunInProgress=True

        self.retVal=None
        #assert self.qOut.empty()
        #assert self.qErr.empty()
        
        if self.shell==False:
            c = self.cmdAndArgsAsIter
        else:
            if self.shellCmdJoin==False:
                c = self.cmdAndArgsAsIter
            else:
                c = " ".join( self.cmdAndArgsAsIter )
        
        
        if self.errToOut:
            errBind = subprocess.STDOUT
        else:
            errBind = subprocess.PIPE
                
        ps = subprocess.Popen(
            self.cmdAndArgsAsIter,
            #stdin=subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = errBind,
            shell=self.shell,
            text=True,
            universal_newlines=True,
        )
        self.ps  = ps
        reader = self.getReaderFunc()

        
        tOut = Thread(target=reader, args=(ps.stdout, self.qOut)  )
        if self.errToOut==False:
            tErr = Thread(target=reader, args=(ps.stderr, self.qErr)  )
        else:
            with io.StringIO() as fakeErr:
                tErr = Thread(target=reader, args=(fakeErr, self.qErr)  )
            
        self.threads.outReader = tOut
        self.threads.errReader = tErr

        ## Actually launch them
        for t in [tOut,tErr]:
            t.daemon=True
            t.start()
            
        return self
    
    def __iterRun(self):
        self.isIterInProgress = True
        self.__runProcAndThreads( )
        
        gotOutChars = []
        gotErrChars = []
        
        threads = self.threads
        threadOut = threads.outReader
        threadErr = threads.outReader
        
        qOut  = self.qOut
        qErr =  self.qErr

        doBreak = False        
        while True:
            outIsAlive = threadOut.is_alive()
            errIsAlive = threadErr.is_alive()
            eitherIsAlive = outIsAlive or errIsAlive
            if not eitherIsAlive:
                if qOut.empty() and qErr.empty():
                    doBreak = True
            
            
            self.moveFromQToList( qOut, gotOutChars )
            self.moveFromQToList( qErr, gotErrChars )
        
            returnStringOut=None
            returnStringErr=None
            
            doSleep=True
            if len(gotOutChars) > 0 :
                returnStringOut = ''.join(gotOutChars)
                self.outList.append( returnStringOut )
                gotOutChars.clear()
                doSleep=False
                
            if len(gotErrChars) > 0 :
                returnStringErr = ''.join(gotErrChars)
                self.errList.append( returnStringErr )
                gotErrChars.clear()
                doSleep=False
            
            if doSleep:
                time.sleep( 0.01 )
            
            if doBreak == True:
                break
            else:
                if returnStringOut is None:
                    returnStringOut=''
                if returnStringErr is None:
                    returnStringErr=''
                yield self.OutErrTuple(returnStringOut, returnStringErr)
        
        ## now out of while loop, yield final one if either remains
        if returnStringOut is not None  or  returnStringErr is not None:
            if returnStringOut  is None:
                returnStringOut=''
            if returnStringErr  is None:
                returnStringErr=''
            yield self.OutErrTuple(returnStringOut, returnStringErr)
            
        self.isIterInProgress = False
        
        ## Cleanup end of iteration
        self.joinProcAndThreads()
        
    def run(self):
        for i in self.iterRun():
            print( i, end='' )
        
tub = Tubprocess( ["python.exe", "example__func__PrintLoop__01_a.py"], ) #errToOut=True )





for i, (out, err), in enumerate(tub):
    print( out, end='' )
    #print( err, end='' )
    if i > 80:
        break
    
print('break')
print( tub.outStr )
time.sleep(1.5)
print( "next" )
print( tub.next().out )
print( "resuming" )



for out, err2 in tub:
    print( out, end='' )
    print( err2, end='' )

print( tub.outStr[-25:] )

#shellTub = Tubprocess( ["python.exe", "example__func__PrintLoop__01_a.py"], shell=True )
#for i in shellTub:
#    print( i.out )


"""
doBreak = False
while True:
    if not t.is_alive():
        if len(linebuffer) == 0:
            doBreak = True
    if linebuffer:
        print( linebuffer.pop(0), end='' )
    else:
        print( "#", end='' )
        time.sleep(1)
    
    if doBreak == True:
        break
"""    

"""
class Tubprocess:
    def __init__(self, *args, **kwargs ):
        self.ps  = subprocess.Popen( *args, **args,
            stdout=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        def is_alive(self):

    def reader(f,buffer):
       while True:
         line=f.read(1)
         if line:
            buffer.append(line)
         else:
            break
            self.threadOut = ()
        self.threadErr()
"""

"""
def reader(buffer, q):
    while True:
        gotChar=buffer.read(1)
        print( f"gotChar: {gotChar}  {type(gotChar)}  " )
        if gotChar != False:
           print("adding to q")
           q.put( gotChar )
        else:
            print()
            ## this won't reach EOF until subprocess closes
            ## read will block instead
            ## so this thread will only end after subprocess ends
            break


x=subprocess.Popen(cmd ,stdout=subprocess.PIPE, universal_newlines=True, text=True)
q=queue.Queue()
t=Thread(target=reader,args=(x.stdout,q))
t.daemon=True
t.start()

charList=[]
doBreak=True
upTo=0
while True:
    if not t.is_alive():
        if q.empty():
            doBreak=True
    
    doBreakOnException=False
    while doBreakOnException:
        try:
            got=q.get(  block=False,timeout=None ) ## same as get_nowait()
            charList.append( got )
        except queue.Empty: ## empty is triggered if blocking when timeout is none
            doBreakOnException = True ## only breaks this inner loop
    
    print( charList[upTo:])
    upTo=len(charList)
        
    if doBreak:
        break
exit()


"""


"""
from io import StringIO
outIo = StringIO()

ps=subprocess.Popen( cmd , shell=False,
    stdout=outIo,
    stderr=outIo,
    universal_newlines=True,
    text=True,
    bufsize=0,
)

doBreak=False
i=-1
while True:
    i+=1
    retVal=ps.poll()
    
    
    print( outIo.getvalue() )
    
    try:
        outs, errs = ps.communicate(timeout=1)
    except subprocess.TimeoutExpired:
        outs, errs = None, None
        ('no new data')
    if outs is not None:
        print( outs, end='' ) 
    #if errs is not None:
    #    print( errs, end='' )
    
    sys.stdout.flush()
    if retVal is not None:
        break

print( "done" )


retVal = ps.wait() ## only needed for its cleanup sidefx         
if retVal == 0:
    self.print( "\n...done" )
"""



 
"""
def readerOld(f,buffer):
    
    optTime=0.01
    sleepTime=1
    
    lastTime=time.time()
    doBreak=True
    while True:
        sleep(5)
        lastTime = time.time()
        gotChar=f.read(1)
        if gotChar:
            buffer.append(gotChar)
            timeTaken = time.time() - lastTime
            if timeTaken < optTime:
                if timeTaken < sleepTime:
                    time.sleep( sleepTime -timeTaken )
                    
        else:
            doBreak =  True
            
        lastTime = time.time
        if doBreak:
            break
"""