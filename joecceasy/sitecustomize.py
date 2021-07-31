from _ast import Or
"""
Check the JoecceasyAutoImport

Env's auto as -1 or less will totally disable auto import,
   as zero will auto import if file has .ezpy extension
   and 1 or greater will enable auto import
   
Env    
"""
import os


def joecceasy_sitecustomize():
    """
    see module level notes
    """
    auto = getAutoFromEnv()
    auto = getAutoByCheckingFileExention(auto)

    if auto>0:
        try:
            import joecceasy
            from joecceasy import Easy
            __builtins__['Easy']=Easy
            __builtins__['Ez']=Easy
        except:
            import traceback
            print("joecceasy module could not be imported")
            print( traceback.format_exc() )    
    
    

    

                    
        


def  getAutoFromEnv():
    ## user env vars should be PascalCase
    ## (upper camel case)  since all caps are just for
    ## system/shell/utils
    ## and lowerCase or snake_case are for
    ## keep in mind, on windows env vars aren't case sensitive
    ## but that shouldn't be a problem unique to us
    ## anyone on windows always has to account for that
    auto = os.environ.get( "JoecceasyAutoImport", False )
    if auto==False:
        auto = os.environ.get( "Joecceasy_auto_import", False )
    if auto==False:
        auto = os.environ.get( "joecceasy_auto_import", False )
    #print( "auto: ", auto )
    
    ## convert auto to integer
    ## (from either False, or the string we got above)
    if auto:
        try:
            auto = int(auto)
        except:
            auto=0
    else:
        auto=0    
    return auto


def getAutoByCheckingFileExention(auto):
    import sys
    #print( sys.argv ) #print( 'sys.argv', sys.argv )
        
    ## if autoload is forced by env, 
    ## we need to check if the script being run ends with
    if auto !=0:
        return auto 
    
    ## now, auto must be zero
    if not len(sys.argv):
        return auto
    
    ##now, auto must be zero and sys.argv must have length
    
    scr = sys.argv[0]
    if not len(scr):
        return auto
    
    
    ## now scr must have len
    chk = scr
    l = []
    chk=chk.rstrip(os.sep)
    if chk.startswith('.'):
        chk=chk[1:]
    
    if not '.e' in chk[-20:]:
        return auto
    
    ## now, scr must be long enough to have one of the
    ## extensions we are looking for 
    if  chk.endswith('.ezpy') or \
        chk.endswith('.ezpyw') or \
        chk.endswith('.easyzpy') or \
        chk.endswith('.easypyw') or \
        chk.endswith('.ezxsh') or \
        chk.endswith('.easyxsh') or \
        False \
        :
        #print( "ended with '.ezpy' ")
        ## only use .ezpy if auto from env isn't -1
        
        ## now, because all above conditions were met,
        ## including the fact that auto must be zero at this point
        ## auto can be turned on
        auto = 1
    
    return auto    


joecceasy_sitecustomize()
