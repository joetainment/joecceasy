"""
The only ones actually needed are:
    posixSignal
        and
    winMsvcrt
    
    most useful ways of calling are:
    
    EasyKeys.Input( prompt, )
    EasyKeys.Input( prompt, timeout, )
    EasyKeys.Input( prompt, timeout, default='it timed out' )
    
    other options and their defaults:
      prependNewline=False
      implementation=None,
      promptEnd=" ",
    
    Easy.KeysMod is this module
    Easy.Keys is his module's EasyKeys class
    
    Easy.Keys    is alias for    Easy.KeysMod.EasyKeys
    
    Easy.Input is alias for Easy.Keys.Input
    
    
"""

import os, sys, time, traceback, unicodedata, re

from . import Utils

from .Utils import EasyExplicitUnsetKwarg

class EasyKeys():
    """
    this is a static class
    """
    
    @classmethod
    def ApplyBackspace( cls, s,
            protectNewlines=True
        ):
        
        return Utils.Funcs.ApplyBackspaces(
            s,
            protectNewlines=protectNewlines
        )
    
    @classmethod
    def ApplyBackspaces(
            cls, s, protectNewlines=True
        ):
        return Utils.Funcs.ApplyBackspaces(
            s,
            protectNewlines=protectNewlines
        )
                
    
    @classmethod
    def FileRead(cls, filePath ):
        return Utils.Funcs.FileRead( filePath )

    
    @classmethod
    def CropListUpToFirstNewline( cls, ls):
        return Utils.Funcs.CropListUpToFirstNewline( ls )

    @classmethod
    def ConsumeAndDiscardRemainingInputOnPosixPlatformViaTermios(cls,
            
        ):
        import re, select, sys, tty, termios, time
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(sys.stdin.fileno())
        tty.setraw(sys.stdin.fileno())
        
        while True:
            found = select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
            if not found:
                break
            else:
                discardThis = sys.stdin.read(1)
                
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



    @classmethod
    def Input(cls, 
            prompt=None, timeout=None,
            default=EasyExplicitUnsetKwarg,   
            implementation=None, promptEnd=" ",
            prependNewline=False, **kwargs,
            #*args, **kwargs
        ):
        if prependNewline:
            print( '' )
        ## use native mode if there's no timeout
        if timeout is None:
            if prompt is not None:
                print(prompt, end=promptEnd, flush=True)
            gotStrViaPyBuiltinInput = input(  )
            return gotStrViaPyBuiltinInput

        if prompt is not None:
            print(prompt, end=promptEnd, flush=True)


        if implementation is None:
            if os.name=='posix':
                implementation='posixSignal'
            elif os.name=='nt':
                implementation='winMsvcrt'
            else:
                implementation='complex'


        got=''
        if False:
            "pass"
        elif implementation in ['winMsvcrt', 'windowsMsvcrt']:
            got = cls.InputOnWindowsPlatformViaMsvcrt(
                timeout=timeout, default=default )            
        elif implementation in ['posixSignal','posix']:
            got = cls.InputBareOnPosixPlatformViaSignal(
                 timeout=timeout, default=default )
        #elif implementation in ['posixTermios']:
        #    got = cls.InputBareOnPosixPlatformViaTermios( timeout=timeout )
        #elif implementation=='posixStopit':
        #    got = cls.InputBareOnPosixPlatformViaStopit(
        #        timeout=timeout, default=default )
        #elif implementation=='posixBash':
        #    got = cls.InputBareOnPosixPlatformViaBash(
        #        timeout=timeout, default=default )
        else:
            ## implementation=='complex':
            raise Exception( 'the requested implementation is unimplemented')
            #got = cls.InputComplex( timeout=timeout, default=default )

        #print('', end=end, flush=True)
        #got = ''.join( got )

        return got



    @classmethod
    def InputBareOnPosixPlatformViaSignal(cls,
            timeout=None,
            default=EasyExplicitUnsetKwarg,
        ):
        end='\n'
        if default is EasyExplicitUnsetKwarg:
            default=''

        import signal

        class AlarmException(Exception):
                    pass

        def alarmHandler(signum, frame):
            raise AlarmException

        def nonBlockingRawInput(timeout,default):
            signal.signal(signal.SIGALRM,
                          alarmHandler)
            signal.alarm(timeout)
            got=default
            try:
                got = input()
                signal.alarm(0)
            except AlarmException:
                ## print a newlin since there was no newline in user input
                #stdin.flush()
                print( '' )     #print('\nPrompt timeout. Continuing.')
                signal.signal(
                    signal.SIGALRM, signal.SIG_IGN)
            return got
        got = nonBlockingRawInput( timeout=timeout, default=default )
        cls.ConsumeAndDiscardRemainingInputOnPosixPlatformViaTermios()
        return got


    @classmethod
    def InputOnWindowsPlatformViaMsvcrt(cls,
            timeout=None, end='\n',
            default=EasyExplicitUnsetKwarg,
        ):
        end='\n'
        if default is EasyExplicitUnsetKwarg:
            default=''
        #print( 'InputOnWindowsPlatformViaMsvcrt' )
        spc=' '
        bytesList=[]
        strList=[]
        if timeout is not None:
            startTime = time.time()
        doBreak=False
        wasTimeoutExpired=False
        while not doBreak:
            newBytesList = cls.KeypressBytesListOnWindowsPlatform( )
            gotBytes = b''.join( newBytesList )
            newStr = gotBytes.decode('utf-8')
            newStr=newStr.replace( '\r', '\n' )
            newStr=newStr.replace( '\b',   '\b' +spc+ '\b' )
            #if not newStr=='':
            #    print( repr( newStr), flush=True  )
            if '\n' in newStr:
                indexFound=newStr.index('\n')
                newStr=newStr[:indexFound]
                if newStr!='':
                    strList.append( newStr )
                    print( newStr.replace('\t',' '), end='', flush=True )
                doBreak=True
            else:
                strList.append( newStr )
                print( newStr.replace('\t',' '), end='', flush=True )
            if ( time.time() - startTime )  >  timeout:
                wasTimeoutExpired=True
                strList.clear()
                doBreak=True
            if doBreak:
                print( '', end=end )
        joinedStr = ''.join(strList)
        ## don't bother applying because done via caller
        # joinedStr = cls.ApplyBackspaces( joinedStr )
        
        if wasTimeoutExpired:
            return default
        else:
            return joinedStr
 
    @classmethod                            
    def KeypressBytesListOnWindowsPlatform(cls, bytesList=None, allCharList=None, doEcho=True ): #echo=True, printFunc=None, callback=None, flush=True, onlyReturnStrings==True):
        """
            will return an empty list if no keys pressed
        """
        if bytesList is None:
            bytesList = []
        if allCharList is None:
            allCharList = []
        if True:
            import msvcrt, os
            while msvcrt.kbhit():
                bytes = msvcrt.getch()
                if bytes==b'\000' or bytes==b'\xe0':
                    bytes = bytes + msvcrt.getch()
                bytesList.append( bytes )
            return bytesList
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

class EasyKeysDisabledOld1():
    """
    """
    
    """      
    @classmethod
    def InputBareOnPosixPlatformViaBash(cls,
            timeout=None,
            default=EasyExplicitUnsetKwarg,
        ):
        end='\n'
        if default is EasyExplicitUnsetKwarg:
            default=''

        
        import os, sys, traceback, tempfile, subprocess

        fhInt, tmpFilePath = tempfile.mkstemp() #suffix=None, prefix=None, dir=None, text=False)
        os.close( fhInt )

        timeoutOptStr = ''
        if timeout is not None:
            timeoutOptStr = ' -t ' + str(timeout+1) + ' '
        
        '''
        mkstemp() returns a tuple containing an OS-level handle to an open file
        (as would be returned by os.open()) and the absolute pathname
        of that file, in that order.
        '''
        
        cmdForBashToRun_Main_OneChar = \
            'read ' + timeoutOptStr +  ' -n 1 -p "type a letter: " ReadResult ; echo -n "$ReadResult"'
            
        cmdForBashToRun_Main_OneLine = \
            'read ' + timeoutOptStr +  ' -p "" ReadResult ; echo -n "$ReadResult"'    
        
        qs="'"
        spc=' '
        cmdBash = "bash" 
        cmdArgs = ("--norc", "--noprofile", "-c")
        cmdForBashToRun_File = tmpFilePath
        cmdForBashToRun = cmdForBashToRun_Main_OneLine + spc + '>' + spc + cmdForBashToRun_File
        #print( cmdForBashToRun )
        #tmpEnv = Easy.Mods.os.environ.copy()
        #del tmpEnv['BASH_ENV']
        wasTimeoutExpired=False
        try:
            subprocess.run(
                [ cmdBash, *cmdArgs, cmdForBashToRun ],  ## gets auto quoted for os sys-like call
                capture_output=False, timeout=timeout
                )
        except subprocess.TimeoutExpired as err:
            print( '', flush=True )
            wasTimeoutExpired=True
            #print( "TIMED OUT" )
            #print( '', end=end, flush=True )
        if wasTimeoutExpired:
            got=default
        else:
            got = cls.FileRead( tmpFilePath )
            os.remove( tmpFilePath )
            print("", end=end, flush=True )
            #print( 'is this doing anythin?' )
            #for i in got:
            #    print( f'got i is: {repr(i)}' )
            got = re.sub(
                r'(\x1b\[|\x9b)[^@-_]*[@-_]|\x1b[@-_]',
                '',
                got, flags=re.I
            )
            #got = re.sub( r'\x1b' + '..' , "", got )
            
        cls.ConsumeAndDiscardRemainingInputOnPosixPlatformViaTermios()
        return got
    

    @classmethod
    def InputBareOnPosixPlatformViaTermios(cls,
            prompt=None, promptEnd=": ", timeout=None,
            default=EasyExplicitUnsetKwarg
        ):
        if default is EasyExplicitUnsetKwarg:
            default=''
        end='\n'
        import re, select, sys, tty, termios, time
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(sys.stdin.fileno())
        tty.setraw(sys.stdin.fileno())
        time.sleep(0.001)
        ch=''
        
        while True:
        
            doBreak=False
            while not dobreak:
                found = select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
                if not found:
                    break
                else:
                    newCh = sys.stdin.read(1)
        
                    if '\x03' in newCh:
                        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                        raise Exception('Control-C Pressed, exiting')
                        sys.exit(1)
                    else:
                        ch=ch+newCh.replace( '\r','\n' )

            if '\n' in ch:
                indexOfFirstNewline = ch.index('\n')
                ch = ch[:indexOfFirstNewline]
                break
            
            if ( time.time() - startTime ) > timeout:
                ch=default
                break
                    
            
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        
        cls.ConsumeAndDiscardRemainingInputOnPosixPlatformViaTermios()
        
        got = re.sub(
            r'(\x1b\[|\x9b)[^@-_]*[@-_]|\x1b[@-_]',
            '',
            got, flags=re.I
        )
        got = cls.ApplyBackspaces( got )
        ch = cls.ApplyBackspaces(ch)
        return ch

    @classmethod
    def InputBareOnPosixPlatformViaStopit(cls,
            timeout=None, default=EasyExplicitUnsetKwarg,
        ):
        end='\n'
        if default is EasyExplicitUnsetKwarg:
            default=''
            
        import stopit
        
        text=''
        @stopit.signal_timeoutable(
            default=default)
        def inputTimeout( ):
            return input()

        got = inputTimeout(timeout=timeout)
        cls.ConsumeAndDiscardRemainingInputOnPosixPlatformViaTermios()
        return got

        #text=''
        #with stopit.ThreadingTimeout(10) \
        #  as to_ctx_mgr:
        #    text=input()
        #return text
    """
    

class EasyKeysDisabledOld2():
    """
    
    """
    """
    @classmethod
    def InputComplex(cls,
            timeout=None,
        ):
        
        if timeout is not None:
            startTime = time.time()
        keyList=[]
        otherList=[]
        cursorOffset=0
        doBreak=False
        #maxIndexCheckedForNewLine=-1
        resultStrList = []
        while not doBreak:
            newKeyList = cls.KeypressList( ) ## don't include a list snce we want a new one
            #print( keyList )
            if len(newKeyList)>0:                
                #print( f'newKeyList is:{repr(newKeyList)}' )
                isNewlineFound = cls.CropListUpToFirstNewline( newKeyList )
                if isNewlineFound:
                    #print( f'found newline!  newKeyList is:{repr(newKeyList)}' )
                    doBreak=True
                ## newKeyList is now cropped, add it to str
                newStr = cls.ListToStr( newKeyList, doApplyBackspace=False)
                if ''!=newStr:
                    resultStrList.append( newStr )   
                    #if len(resultStrList)>0:
                    #print( f' resultStrList repr is: {repr(resultStrList)}' )
            
            if timeout is not None:
                if (time.time() - startTime) > timeout:
                    print( '', flush=True ) ## end='\n' used as default
                    doBreak=True
                    
        got = ''.join( resultStrList )
        
        got = re.sub(
            r'(\x1b\[|\x9b)[^@-_]*[@-_]|\x1b[@-_]',
            '',
            got, flags=re.I
        )
        got = cls.ApplyBackspaces( got )
        return got
    
            
    
    @classmethod
    def ListToStr( cls, ls,
            ignoreNonStr=True,
            doApplyBackspace=True,
            doReplaceReturns=True
        ):
        '''
          also removes unwanted because t simply ignores them!
        '''
        s = cls.ListToStrRaw( ls, ignoreNonStr=ignoreNonStr )
        
        if doReplaceReturns:
            s = cls.ReplaceReturns(s)
            
        if doApplyBackspace:
            s = cls.ApplyBackspace(s)
            
        return s
        
    @classmethod
    def ListToStrRaw( cls, ls, ignoreNonStr=True ):
        '''
            gather all items in a list together into a new string
            without any other replacements
            
            normally it ignores items that aren't string like (ignoreNonStr=True)
            
            ignoreNonStr, if off, wiil cause errors if list being
                converted contains non str like objs
        '''
        if ignoreNonStr:
            n = [ v   for v in ls   if isinstance(v,str)  ]
            return ''.join(n)
        else:
            return ''.join(ls)
    
    @classmethod
    def CondenseStrInList( cls, origList, affectOrig=False ):
        if affectOrig:
            inList=origList.copy()
            origList.clear()
            outList = origList
        else:
            inList=origList
            outList=[]
        q = []
        for v in ls:
            if isinstance(v, str):
                q.append( v )
            else:
                if len(q)>0:
                    outList.append( ''.join(q) )
                outList.append( ''.join(q) ) 
                outList.append( v )
        if len(q)>0:
                    outList.append( ''.join(q) )
        return outList
    
    @classmethod
    def ReplaceReturns(cls, s ):
        return s.replace( '\r' , '\n' )
    
    @classmethod
    def RemoveUnwantedChars(cls, s, 
            protectBackspace=True,
            protectWhitespace=True,
            #protectNewline=True,
            doApplyBackspace=True,
            doReplaceReturns=True,
        ):
        
        s = cls.RemoveControlChars(
            s,
            protectBackspace=protectBackspace,
            protectWhitespace=protectWhitespace,
            #protectNewline=protectNewline,
        )
        
        if doApplyBackspace==True:
            s = cls.ApplyBackspaces( s )
        
        if doReplaceReturns:
            s = cls.ReplaceReturns( s )
            
        return s
    
    
    @classmethod
    def RemoveControlChars(cls, s,
            protectBackspace=False,
            protectWhitespace=False,
            #protectNewline=False,
        ):
        '''
        given a string, return a string without the control characters
        '''
        import unicodedata
        
        ls = []
        
        for ch in s:
            #print( f'ch type is:{type(ch)}  and ch is:{repr(ch)}')
            wasControlChar = unicodedata.category(ch)[0]=="C"
            wasNotWhiteSpace = not str.isspace(ch)
            wasNotBackspace = ch!='\x08'
            #wasNotNewLine = ch!='\n'
            
            if (        wasControlChar
                    and (wasNotWhiteSpace or protectWhitespace==False)
                    and (wasNotBackspace or protectBackspace==False)
                    #and (wasNotNewLine or protectNewline==False) #newline covered by whitespace
                ):
                "pass"
                #print(f'removable control character found: {repr(ch)}')
            else:
                ls.append( ch )
        return ''.join( ls )

    @classmethod
    def RemoveControlCharacters(cls, s):
        import unicodedata
        if not isinstance( s, str ):
            raise Exception( 'function must be passed a string as an argument' )
        rs = "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")
        return rs

    @classmethod
    def KeypressList( cls, mixedList=None, doEcho=True, keepNonStr=True
        ):
        if os.name=='nt':
            return cls.KeypressListOnWindowsPlatform(
                mixedList=mixedList,
                doEcho=doEcho,
                keepNonStr=keepNonStr,
            )
        else:
            return cls.KeypressListOnPosixPlatform(
                mixedList=None,
                doEcho=True,
                keepNonStr=keepNonStr,
            )

    @classmethod
    def KeypressListOnWindowsPlatform( cls,
            mixedList=None, keepNonStr=False, flat=False,
            doReplaceReturn=True,
            doEcho=True,
            #doApplyBackspace=True,
            #allCharList=None,
        ):
        '''
            will return an empty list if no keys pressed
            or a list that has both
        '''
        if mixedList is None:
            mixedList = []
        bytesList = cls.KeypressBytesListOnWindowsPlatform( )
        i=0
        if len(mixedList)>0:
            if isinstance( mixedList[-1], str ):
                lastStr = mixedList.pop()
                q = [ lastStr ]
            else:
                q = []                
        else:
            q = []
            
        if False: #keepNonStr==False:
            for v in mixedList:
                if isinstance( v, str ):
                    q.append(v)
            mixedList.append( ''.join( q ) )
            return mixedList
        
        else:    
            for bytesChunk in bytesList:
                if (     bytesChunk[0]==224
                      or bytesChunk[0]==0
                    ):
                    if len(q)>0:
                        mixedList.append( ''.join(q) )
                    q.clear()
                    if keepNonStr==True:
                        mixedList.append( bytesChunk )
                else:
                    try:
                        s = bytesChunk.decode("utf-8")
                        if doReplaceReturn:
                            s=s.replace( '\r', '\n' )
                        spc=' '
                        echoFix = s
                        echoFix = echoFix.replace(
                            '\x08',
                            '\x08' +spc+ '\x08'
                        )
                        #echoFix = echoFix.replace(
                        #'\n', '\n'+('\b'*8) )
                        #+' '+'\x08' )

                        print( echoFix, end='', flush=True  )
                        q.append( s )
                    except UnicodeDecodeError as err:
                        if len(q)>0:
                            mixedList.append( ''.join(q) )
                        q.clear()
                        if keepNonStr==True:
                            mixedList.append( bytesChunk )
                if flat==True:
                    for c in q:
                        mixedList.append( c )
                    q.clear()
                    
            if len(q)>0:
                mixedList.append( ''.join(q) )
            return mixedList
    
    @classmethod            
    def KeypressListOnPosixPlatform(cls, mixedList=None, doEcho=True,  keepNonStr=False, ):
        if mixedList==None:
            mixedList=[]
        import re, select, sys, tty, termios, time
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setcbreak(sys.stdin.fileno())
        tty.setraw(sys.stdin.fileno())
        time.sleep(0.001)
        ch=''

        while True:
            found = select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
            if not found:
                break
            else:
                ch = ch + sys.stdin.read(1)
                time.sleep(0.02)
                
        if len(ch)>0:
            if not isinstance( ch, str):
                raise Exception('Major Error, keypress char was expected to be a str')
            if ch == '\x03':
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                raise Exception('Control-C Pressed, exiting')
                sys.exit(1)
                #re.compile(r''' \x1B # ESC (?: # 7-bit C1 Fe (except CSI) [@-Z\\-_]  ''')
            else:
                patCodes=re.compile(
                #    #r"(\x1b\[|\x9b)[^@-_]*[@-_]|\x1b[@-_]",
                    r'(\x1b\[|\x9b)[^@-_]*[@-_]|\x1b[@-_]',
                    flags=re.I,
                )
                ch=patCodes.sub('', ch)
                patReaesc = re.compile(r'\x1b[^m]*m' )
                ch = patReaesc.sub('', ch )
                ch=ch.replace( '\u007f', '' )
                # match nothing test #pat=re.compile( '(?!)' )  #r''' \x1B # ESC (?: # 7-bit C1 Fe (except CSI) [@-Z\\-_]  ''' )
                # ch = pat.sub( '', ch)
                #assert len(ch)==1
                
                if ch == '\x7f':
                    ch = '\x08'
                if ch == '\r':
                    ch = '\n'
                #if ch=='\n':
                #    raise Exception('delme ')
                if len(ch)==1 and doEcho:
                    echoFix=ch
                    echoFix = echoFix.replace('\x08', '\x08'+' '+'\x08' )
                    echoFix = echoFix.replace('\n', '\n'+('\b'*800) ) #+' '+'\x08' )
                    print( echoFix, end='', flush=True  )
                if len(ch)==1:    ##>0 and len(ch<2:
                    cls.AppendOrConcatWithLastStr( mixedList, ch )
                
                #sys.stdin.flush()
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return mixedList
    
    @classmethod
    def DeleteThisBrokenFunc(cls):
        ''' Returns True if a keypress is waiting to be read in stdin, False otherwise.
        '''
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            import select
            dr,dw,de = select.select([sys.stdin], [], [], 0)
            found =  ( dr != [] )
            if found:
                print( f'is found:{found}' )
            return found
        
    @classmethod                            
    def KeypressStr(cls, doApplyBackspace=True, convertReturnToNewline=True ):
        keyList = cls.KeypressList(
            convertReturnToNewline=convertReturnToNewline,
        )
        if doApplyBackspace:
            s = cls.ApplyBackspace( s )
        return s
    

    @classmethod                            
    def KeypressBytesListOnPosixPlatform(cls, bytesList=None, allCharList=None, doEcho=True ): #echo=True, printFunc=None, callback=None, flush=True, onlyReturnStrings==True):
        
        if True:
            import sys, select, tty, termios
            def isData():
                return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
            doBreak=False
            wasError=False
            while True:
                sys.stdout.flush()
                c = None
                tbToPrint = None
                #print('-', end='')         
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setcbreak(sys.stdin.fileno())
                    time.sleep(0.01)
                    if isData():
                        c = sys.stdin.read(1)
                    else:
                        doBreak=True
                except:
                    wasError=True
                    doBreak=True
                    tbToPrint=traceback.format_exc()
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                #print( f' c:{c}', end='')
                if wasError:
                    print( 'an error occured' )
                if tbToPrint is not None:
                    print( tbToPrint ) 
                if c is not None:
                    #print( f'\nc is: {c}' )
                    #sys.stdout.flush()
                    allCharList.append(c)
                    #if c=='\x08':
                    #    c='\b'
                    #print( repr(c), end='' )
                    sys.stdout.flush()
                    if type(c) == str and len(c)==1:
                        #print( len(c) )
                        b = c.encode('utf-8')
                        print( repr(c) ) #, end="" )
                        print( repr(  b.decode(    'utf-8'    )  ) ) #, end="" )
                        #sys.stdout.flush()
                        bytesList.append( b )
                    else:                        
                        print( f'c is not a string, it is a: {type(c)} and is {repr(c)}')
                        print( f'None', end="" )#repr(b) )
                        sys.stdout.flush()
                if doBreak:
                    break
            return bytesList
        #raise Exception( 'platforms other than windows not implemented yet' )
            
    """



## oldCodeThatWasUnderInputComplex
"""        
                else: ## last is a string
                    if not '\n' in last:
                        ""  # doesn't have newline, so do nothing
                    elif '\n'==last:
                        newKeyList.pop()
                        doBreak=True
                    elif '\n' in last:
                    else: #'\n' in last but not all of last
                        gather=''
                        for c in last:
                            if c!='\n':
                                gather=gather + c
                            else:
                                break
                        newKeyList[ -1 ] = gather
                        doBreak=True
                        
                        
                        lastSplit = last.split('\n')
                        ## if there's something else before first \n
                        ## use only that chunk
                        if len(lastSplit)>0:
                            last=lastSplit[0]
                            newKeyList[ -1=last ]
                        else:
                            ## otherwise, just remove
                            ## the item from list
                            ## since item has nothing useful
                            newKeyList.pop()
                            # redundant  # last = ''
                    ## last doesn't contain newline at all
                    else:
                            
                            
                    last = last.split('\n')[0]
                    last = last.rstrip('\n')
                    if '\n' in lastInList:
                        if '\n'==lastInList:
                            
                        else:
                        str.rstrip
                    while item.endswith
                    break
            if (time.time() - startTime) > timeout:
                tooLong=True
                break
            s = cls.ListToStr( newKeyList, doApplyBackspace=False)
            return s
"""
            
"""
            bs = '\x08'
            spc = ' '
            #sys.stdout.flush()
            for c in s:
                #if not c.isspace():
                #print( repr(c) )
                if c == '\t':
                    print(spc, end='')
                    cursorOffset+=1
                    sys.stdout.flush()
                elif c==bs:
                    if cursorOffset>0:
                        print( bs + spc + bs, end="" )
                        cursorOffset-=1
                        sys.stdout.flush()
                else:
                    cursorOffset+=1
                    print( c, end="" )
                    sys.stdout.flush()

            
            ## add to keyList if not already
            if len( s ) > 0:
                #print( "s had length")
                lastStr=""
                if len( keyList )>0:
                    if isinstance( keyList[-1], str ):
                        lastStr = keyList.pop()
                        rs = lastStr + s
                        keyList.append( rs )
                    else:
                        rs = s
                        keyList.append( rs )
                else:
                    rs=s
                    keyList.append( rs )
            
            tooLong = False
            if timeout is not None:
                if (time.time() - startTime) > timeout:
                    tooLong=True

            if '\n' in s  or  '\r' in s or tooLong:
                resultStr =  cls.ListToStr( keyList )
                ## don't actually return a newline at the end
                while resultStr.endswith('\n'):
                    resultStr = resultStr[:-1]
                return resultStr
            else:
                time.sleep(0.002)
"""
