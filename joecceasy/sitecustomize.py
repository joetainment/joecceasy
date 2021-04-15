def joecceasy_sitecustomize():
    import os, sys, traceback
    #print( sys.argv )
    ## Env's auto as -1 or less will totally disable auto import,
    ##   as zero will auto import if file has .ezpy extension
    ##   and 1 or greater will enable auto import
    auto = os.environ.get( "joecceasy_auto_import", False )
    #print( "auto: ", auto )
    if auto:
        try:
            auto = int(auto)
        except:
            auto=0
    else:
        auto=0
    #print( 'sys.argv', sys.argv )
    ## we need to check if the script being run ends with 
    if len(sys.argv):
        #print( "sys.argv has non-zero length" )
        scr = sys.argv[0]
        chk = scr
        l = []
        chk=chk.rstrip(os.sep)
        if chk.startswith('.'):
            chk=chk[1:]
        if chk.endswith('.ezpy') or chk.endswith('.ezpyw'):
            #print( "ended with '.ezpy' ")
            ## only use .ezpy if auto from env isn't -1
            if auto>-1:
                auto=1
    if auto>0:
        try:
            import joecceasy
            from joecceasy import Easy
            __builtins__['Easy']=Easy
            #Easy.Init( shouldAutoLoadCode=False )
            #print( "autoimported!")
        except:
            print("joecceasy module could not be imported")
            print( traceback.format_exc() )    
joecceasy_sitecustomize()
