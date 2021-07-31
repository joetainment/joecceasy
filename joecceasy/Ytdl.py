import os, sys, traceback
from joecceasy import Easy

import youtube_dl
import pdb

class YtResult:
    def __init__( self ):
        self.check=False
        self.url=None
        self.attempStartTimeStr = Easy.NowLocalStr()
        self.workDir = None
        self.dlFname = None
        self.fname=None
        self.txtFile = None
        self.resultEx = None ## result obj from extracted info stage
        self.resultDl = None ## result obj from dl stage
        self.resultEntries = []

    def get( *args):
        if len(args)==2:
            key = args[0]
            default = args[1]
            if hasattr(self, key):
                return self[key]
            else:
                return default
        elif len(args)==1:
            return self[key]
        else:
            raise ( "YtResult.get needs 1 or two args."
                    + " 1 args to get by key strictly,"
                    + " 2 args to get by key with fallback."
            )

    def __getitem__(self, idx ):
        ### consistency - convert idx a[b] to tuple
        #if not isinstance(idxs, tuple):
        #    idxs = tuple(idxs)
        #print( 'getting by index' )
        if hasattr( self, idx ):
            ret = getattr( self, idx )
        else:
            ret = self.resultEx[idx]
        return ret

class YtResults:
    'pass'

class FakeExitError(Exception):
    pass

class CheckerError(Exception):
    pass

class Checker():
    def __init__(self, location):
        self.location=location

    def check( self, id ):
        ## clean up id in case it has other data in it
        if '&' in id:
            ampAt=id.index('&')
            id = id[:ampAt]
        location = self.location
        listed = Easy.Ls( location )
        #print( f'listed: {listed}')
        isOk = True
        for l in listed:
            #print( f'comapre  id: {id}   l: {l}' )
            if id+'.' in l or l.endswith(id) or f'?id={id}' in l or f'&id={id}' in l:
                isOk = False
        return isOk


def dprint(d):
    #'pass'
    #print( d )
    for k in d: #,v in d.items():
        print( k )

def ytGetPlaylistIds( url ):
    urls = []
    
    ydl_opts = {
        #'merge_output_format':'mkv',
        'extract_flat':True,
        'ignoreerrors': True,
    }
    with youtube_dl.YoutubeDL( ydl_opts ) as ydl:
        playd = ydl.extract_info(url, download=False)
        for v in playd['entries']:
            urls.append( v['id'] )
        return urls
    
    """
        ydl_opts = {
            #'merge_output_format':'mkv',
            'extract_flat':True,
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        result = ydl.extract_info(url , download=False)


        if 'entries' in result:
            entries = result['entries']
            #if maxEntries < 0:
            #    pass
            #elif maxEntries == 0:
            #    entries=[]
            #else:
            #    entries=entries[:maxEntries]
            for entry in entries:
                #print( entry )
                try:
                    eUrl = entry['webpage_url']
                except:
                    eUrl = 'https://www.youtube.com/watch?v=' + entry['id']
                urlsExtarctedToDownload.append( eUrl )
                print( eUrl )
                resultsList.extend( eUrl )
    """

def _ytDownload( url, location=None, checkFunc=None, resultsList=None, maxEntries=-1 ):
    """
    this is the lower level downloading func
    it shouldn't be used directly
    """
    dirAtFunStart = Easy.Cwd
    if location is None:
        location = Easy.Cwd
    nowStr = Easy.NowLocalStr()
    workDir = Easy.TmpDir( dir=location, prefix='01--working--'+nowStr )
    Easy.Cd( workDir )

    urlsExtarctedToDownload = []
    if resultsList is None:
        resultsList = []

    ret = YtResult()
    ret.attempStartTimeStr = nowStr
    ret.url = url
    ret.workDir=workDir
    
    try:

        ## Check for early skip
        if True:  ##'v=' in url:
            ## easiest checks are for id as parts after 'v='
            ## or just as part after last slash
            uEnd = url.split('/')[-1]
            uEnd = uEnd.split('?v=')[-1]
            uEnd = uEnd.split('&v=')[-1]
            ## if we've chopped off the end via slash or v=
            ## then if it's a simple video, it shouldn't have '?'
            ## in it
            if checkFunc is not None and not '?' in uEnd:
                if not checkFunc( uEnd ):
                    #print( f'early skip: {url}' )
                    raise CheckerError( 'Early skip! check failed on id: ' + str(uEnd) )
        tmpUrl=url
        if '&' in url:
            urlSplit = url.split('&')
            loopI = len(urlSplit) - 1
            while loopI >= 0:
                listPart = urlSplit[loopI]
                if loopI > 0 and urlSplit[loopI].startswith('list='):
                    del urlSplit[loopI]
                loopI -= 1
            tmpUrl='&'.join( urlSplit )
        print( tmpUrl )
        
        ydl_opts = {
            #'merge_output_format':'mkv',
            #'extract_flat':True,
            'extractaudio':True,
            'noplaylist':True,
            #'audio_only':True,
            'restrict_filenames':True,
            #'no_overwrites':True,
            #'no_post_overwrites':True,
            'keepvideo' : False,
            #'extract-audio' : True,
            'quiet':False,
            #'noplaylist':True,
            #'get_filename':True,
            #'progress_hooks': [my_hook],
                #def my_hook(d):
        }
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        #pdb.set_trace()
        result = ydl.extract_info( tmpUrl , download=False) ## tmpUrl to ensure not a list!
        #pdb.set_trace()
        ret.resultEx = result
        if 'entries' in result:
            raise "handling of playlists/channels is disabled currently"
            ## old playlist handling code was here, moved to end of this file for reference
        else:
            fname = ydl.prepare_filename(result)
            title = result['title']
            id=result['id']
            acodec=result['acodec']
            ext=result['acodec']
            if checkFunc is not None:
                if not checkFunc( id ):
                    raise CheckerError( 'Check failed on id: ' + str(id) )
            else:
                    ret.check = True
            ## This is a hack to prevent youtube_dl from running sys.exit
            oldSysExit=sys.exit
            def fakeExit(arg):
                raise FakeExitError
            sys.exit = fakeExit
            try:
                youtube_dl.main([
                    url,
                    '--extract-audio' ,
                    '--no-playlis',
                ])
            except KeyboardInterrupt as err:
                oldSysExit(1)
                raise err
            except FakeExitError:
                'pass'
                #print( 'sys.exit was prevented' )
            sys.exit = oldSysExit


            ## if we were able to dl a file
            ## find name, fix name, move files
            files = Easy.Ls( Easy.Cwd )
            if not len(files):
                print( f'Error, unable to download url: {url}')
            else:
                dlFname = files[0]
                ret.dlFname = dlFname
                #print( f'dlFname: {dlFname}' )
                fixedName = Easy.Mods.re.sub(r'[^\x00-\x7f]',r'', dlFname )
                if dlFname!=fixedName:
                    os.rename( dlFname, fixedName )  ## make Easy.Rename
                os.rename(
                    fixedName,
                    os.path.join(
                        location, fixedName
                    )
                )
                ret.fname = fixedName
                ret.txtFile = os.path.join(
                        location, fixedName ) + '.alreadyDownloaded.txt'
                if not os.path.exists( ret.txtFile ):
                    with open( ret.txtFile, 'w' ) as txtFh:
                        import json
                        metadata = {}
                        metadata['date_of_dl'] = Easy.NowLocalStr()
                        metadata['title'] = title
                        json.dump( metadata, txtFh )
                        #txtFh.write( 'already downloaded' )
    ## This gets triggered if the checkFails,
    ## in which case most of the above code never runs
    ## since it would be after the CheckerError
    except CheckerError as err:
        pass
    ## Really important to handle keyboard errors! For quit with Ctrl-c
    except KeyboardInterrupt as err:
        raise err
    ## On most other errors we just continue after printing a warning
    except:
        Easy.PrintTraceback()
        print('continuing anyway...')
    finally:
        ## really important we go back to original directory!
        Easy.Cd( dirAtFunStart )
        try:
            os.rmdir( workDir )
        except:
            ## something is really wrong in this case, so we don't continue on
            print( f"Couldn't delete tmp dir: {workDir}" )

        ## regardless of whether our result has much useful data in it, we add the result
        resultsList.append( ret )
        ## return the same list we were given, but modifed, with YtResult added
        return resultsList

## results list is non-optional for this one since it should be provided by caller
def ytdlIter( urls, resultsList, location=None, checkFunc=None,maxEntries=-1, forceList=False ):
    if isinstance(urls, str):
        urls = [urls]
    if location is None:
        location=Easy.Cwd
    if checkFunc is None:
        checker = Checker(location)
        checkFunc=checker.check
    for url in urls:
        #print( 'iterating...' )
        if (    forceList==True
                or (
                    ( "?list=" in url or "&list=" in url)
                    and not  ('?v=' in url or '&v=' in url)
                )
                or '/c/' in url
                or url.endswith('/videos')
                or url.endswith('/featured')
                or ('/user/' in url  and  (not '&v=' in url or '?v=' in url) )
            ):
            try:
                #print( f'treating as playlist: {url}' )
                ids = ytGetPlaylistIds( url )
                #print( f'Adding to urls from id list found in playlist... ')
                  ##, id list was: {ids}' )
                for id in ids:
                    urls.append( 'https://www.youtube.com/watch?v='+id )
            except KeyboardInterrupt as err:
                raise err
            except:
                Easy.PrintTraceback()
        else:
            try:
                _ytDownload(
                    url,
                    resultsList=resultsList,
                    location=location,
                    checkFunc=checkFunc
                )
                #print( 'try end' )
            except KeyboardInterrupt as err:
                raise err                                    
            except:
                Easy.PrintTraceback()
        #print( 'yielding' )
        yield resultsList



def ytdl( urls, resultsList=None, location=None, checkFunc=None,maxEntries=-1, forceList=False ):
    if resultsList is None:
        resultsList = []
    yIter = ytdlIter(urls,
        resultsList,
        location=location,
        checkFunc=checkFunc,maxEntries=maxEntries, forceList=forceList
    )
    #print( 'pre iter' )
    for resultsListKeepsBeingReturned in yIter:
        ret = resultsListKeepsBeingReturned
    #    print( 'after return' )
    return ret


"""

            #print( "result: ")  #dprint( result ) #channeltitle = result['chan']
            #print( f'id: {id}' ) #print( f'acodec: {acodec}' )  #print( f'fname: {fname}' )


                #print( f'fixedName: {fixedName}')
                #ret = fixedName

                #print(ext)
                #import ffmpeg
                #f = ffmpeg
                #inp  = f.input(fname)
                #a = inp.audio
                ##.hflip()
                #f.output( a, f'{fname}.{ext}', {'c:a':'copy'})  #**{'vn':True,'sn':True,'c:a':'copy'})
                #f.run()
                #ydl2 = youtube_dl.YoutubeDL(ydl_opts)
                #print( f'url: {url}' )
                #downloaded = ydl2.download( [url] )
                #print( type(downloaded) )






## old playlist handling code
if False:
                print( 'entries were found, recursively downloading urls in playlist/channel' )
                entries = result['entries']
                ret.entries = entries
                if maxEntries < 0:
                    pass
                elif maxEntries == 0:
                    entries=[]
                else:
                    entries=entries[:maxEntries]
                ytResult.entries = result
                for entry in entries:
                    #print( entry )
                    try:
                        eUrl = entry['webpage_url']
                    except:
                        eUrl = 'https://www.youtube.com/watch?v=' + entry['id']
                    urlsExtarctedToDownload.append( eUrl )
                    #print( eUrl )
                    resultsList.extend(
                        _ytDownload(eUrl, location,
                                    checkFunc=checkFunc,
                                    resultsList=resultsList,
                                    maxEntries=maxEntries )
                    )





"""
