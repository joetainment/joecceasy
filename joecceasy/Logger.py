from . import Utils
classproperty = Utils.classproperty
class Logger:
    @classproperty
    def Logging(cls):
        import logging
        return logging
    

    @classmethod
    def Log(cls, msg, *args, **kwargs):
        if 'level' in kwargs:
            level = kwargs['level']
        else:
            import logging
            level=logging.getLogger().getEffectiveLevel()
        return cls.LogN( level, msg, *args, **kwargs )
    
    @classmethod     ## for some reason, as @classproperty caused problems w *args, **kwargs
    def LogFormatDisable(cls, format='' ):
        import logging
        #logging.basicConfig(format=format)
        l=logging.getLogger()
        cls.LogOldFormatters = []      
        if not len(l.handlers):
                oldDisableLevel = l.manager.disable ## no logging.getDisable() so get manually
                logging.disable( 99999 )
                logging.log( 50, "this won't show due to being disabled")
                logging.disable( oldDisableLevel )
        for h in l.handlers:
            cls.LogOldFormatters.append( h.formatter )
            h.setFormatter( '' )
            
    @classmethod
    def LogFormatEnable(cls, format=None ):
        import logging
        l=logging.getLogger()
        for i,h in enumerate( l.handlers ):
            h.setFormatter( cls.LogOldFormatters[i] )
            #h.setFormatter( '' )
        
            
    @classproperty
    def LogFormatCtx(cls, format='' ):
        """
        currently unimplemented because
        ## hackish, due to use of private-like var   _fmt
        """
        @cls.ContextManager
        def swapper(*args,**kwargs):
            import logging
            l=logging.getLogger('')
            old = []
            #logging.log( 50, '', )
            if not len(l.handlers):
                oldDisableLevel = l.manager.disable ## no logging.getDisable() so get manually
                logging.disable( 99999 )
                logging.log( 50, "this won't show due to being disabled")
                logging.disable( oldDisableLevel )
            for h in l.handlers:
                #print( dir(h.formatter) )
                #print( f'was: {h.formatter._fmt}')
                old.append( h.formatter )
                h.setFormatter('')
            yield l
            
            for i, h in enumerate( l.handlers ):
                h.setFormatter( old[i] )
                #print( f'restored: {h.formatter._fmt}')
            
            return l
        return swapper
    
    @classmethod
    def Llog( cls, msgs, args=[], kwargs={} ):
        for msg in msgs:
            cls.Log( msg, ) # *args, **kwargs
            
    @classmethod
    def LlogN( cls, _level, msgs, args=[], kwargs={} ):
        for msg in msgs:
            cls.LogN( _level, msg, ) # *args, **kwargs
    
    @classmethod
    def LogN(cls, _level, msg, *args, **kwargs):
        """
        Easy.LogN( 50, "my msg" )
          the level will be overridden, uses default logger
          unless it's None, which will fallback to loggers effective level
          if its logging.NOTSET then fallback to logging.INFO 20 if it
        """
        import logging
        n = _level
        if n is None:
            l=logging.getLogger()
            n=l.getEfftectiveLevel()
            if n==logging.NOTSET:
                n==logging.INFO
        if 'level' in kwargs:
            del kwargs['level']
        #cls.See('kwargs')
        #cls.See('args')
        #cls.See('nLevel')
        #args=list(args)
        logging.log( n, msg, *args, **kwargs)
        #r=   ## logging doesn't return anything so unneccesary
        #Easy.Ic( r )
        #return r


    @classmethod
    def LogSetLevel(cls, level):
        import logging
        l=logging.getLogger('')
        l.setLevel( level )
        
    @classmethod
    def LogGetDefaultLogger(cls):
        import logging
        return logging.getLogger()
        
    
        
    
    """
    @classmethod
    def Logger(cls, default=info, ):
        import logging
        n = cls.Namespace()
        ## these are simplified levels,
        ## not the real ints since error int is actually 40 etc
        simpleIntsToLevels = {
            0:'debug',
            1:'debug',
            2:'info',
            3:'warning',
            4:'error',
            5:'critical',
        }
        simpleLevelsToInts = {}
        for k,v in intsToLevels.items():
            levelsToInts[v]=k
            
        if isinstance( level, int):
            level = simpleIntsToLevels[]
            
        ##
        intsToLevels = {
            50='critical'
            40='error'
            30='warning'
            20='info'
            10='debug'
            0='notset'
        }
        assert logging.CRITICAL=50
        assert logging.ERROR=40
        assert logging.WARNING=30
        assert logging.INFO=20
        assert logging.DEBUG=10
        assert logging.NOTSET=0
        
        n.simpleIntsToLevels = simpleIntsToLevels
        n.simpleLevelsToInts = simpleLevelsToInts
        n.l1=logging.debug
        n.l2=logging.debug
        n.l3=logging.warning
        n.l3=logging.error
        n.l3=logging.critical
        n.l0=[l1,l2,l3,l4,l5] ## this one is zero based index
        n.l=[ l1,l1,l2,l3,l4,l5 ] ## this one has indexes that match levels
        
        n.log = cls.Log
        return n  ## return the new loger object
    
    #@def
    """
