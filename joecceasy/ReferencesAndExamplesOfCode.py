
class ExampleClass01Meta(type):
    ## __setattr__ and __getattr__ can potentially cause issues
    ## such as recursions (they introduce serious complexity)
    '''
    def __setattr__(cls, key, val ):
        if key=='P':
            print( val )    
        #else:
        #    setattr( cls, key, val)  ## recursion issues
    '''  