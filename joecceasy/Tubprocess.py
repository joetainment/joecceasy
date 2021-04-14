import collections, io, queue, subprocess, sys, time
from threading import Thread

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
                errToOut=False, autoPrint=False,
                ## old extra args:   autoRun=False
            ):               
        self.cmdAndArgsAsIter = cmdAndArgsAsIter
        self.sleep = sleep                 
        
        self.shell=shell
        self.shellCmdJoin=shellCmdJoin
        
        self.errToOut = errToOut
        self.autoPrint = autoPrint
        
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
                if self.autoPrint:
                    print( returnStringOut, end='' )
                gotOutChars.clear()
                doSleep=False
                
            if len(gotErrChars) > 0 :
                returnStringErr = ''.join(gotErrChars)
                self.errList.append( returnStringErr )
                if self.autoPrint:
                    print( returnStringOut, end='' )
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
    
    def wait(self):
        for i in self:
            "pass"
        return self.retVal
    
    def run(self):
        return self.wait()
