
def test_Utils_Funcs_Fstring_01():
    from joecceasy import Easy
    
    exampleToFormat = "example number is: {number}"
    ## note that at this point the substitution hasn't happened yet
    
    ## now number is defined, late
    number = 2
    
    ## now we want to use our number, late
    result = eval( Easy.Fstring( exampleToFormat ) )
    
    ## at this point the substitution should be done
    
    ## here's the normal python way
    resultPyFmt = exampleToFormat.format( **locals() )
    
    #print ( f'pure python example: {resultPyFmt}'  )
    assert resultPyFmt == result



def test_Utils_funcs_Fstring02():
    from joecceasy import Easy
    
    exampleToFormat = "example number is: {number}"
    ## note that at this point the substitution hasn't happened yet
    
    ## now number is defined, late
    number = 5
    substitutions={ 'number': number }
    
    ## print while substituting in local variables and capture result...
    r1 = Easy.PrintWithFormat( exampleToFormat, **locals() )
    ## or, substituting named filed with given value..
    r2 = Easy.PrintWithFormat( exampleToFormat, number=number )
    ## alternate methods of doing the same, with optional end
    r3 = Easy.PrintWithFormatV( exampleToFormat, kwargs=locals(), end='\n\n\n' )
    
    # we don't have to print the results
    r4 = Easy.Format( exampleToFormat, number=5 )
    r5 = Easy.FormatV( exampleToFormat, kwargs=substitutions )
    # or without, keyword arguments, first locals then globals, use None to skip
    r6 = Easy.FormatV( exampleToFormat, None, substitutions )
    
    resultPyFmt = exampleToFormat.format( **locals() )
        ## nothing wrong with this other than too much syntax
    #print ( f'pure python example: {resultPyFmt}'  )
    assert resultPyFmt==r1
    assert resultPyFmt==r2
    assert resultPyFmt==r3
    assert resultPyFmt==r4
    assert resultPyFmt==r5
    assert resultPyFmt==r6
