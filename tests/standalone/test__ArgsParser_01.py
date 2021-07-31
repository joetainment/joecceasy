from joecceasy import Easy

def test_ArgParser_01():
    ## this should eventually be triggered by pytest and actually
    ## call cmd line python with arguments to test, then check results
    utiltest_ArgParser_01()
    
def utiltest_ArgParser_01():
    """
    run the command and test the result
    python "test__ArgsParser_01.py" "positional arg a" "positional arg b" "positional arg c" --myStringArg "this is my string!" --myFlagArg --myFloatArg 0.3 --myIntArg 7
    """
    #Easy.ArgsParser.GetFlag("f")
    #print( Easy.ArgsParser.GetFlag("testArg") )
    #print( )
    print("THIS TEST DOESN'T WORK WHEN AUTO RUNNING ALL TESTS BY FILE EXTENSION")
    name = "myPositionalArg"
    print( f'positional arg is: ',
        Easy.ArgsParser.GetNargs( 0 )
    )
    name = "myStringArg"
    print( f'{name} is: ',
        Easy.ArgsParser.GetStr(name)
    )
    name = "myIntArg"
    print( f'{name} is: ',
        Easy.ArgsParser.GetInt(name)
    )
    name = "myFloatArg"
    print( f'{name} is: ',
        Easy.ArgsParser.GetFloat(name)
    )
    name = "myFlagArg"
    print( f'{name} is: ',
        Easy.ArgsParser.GetFlag(name)
    )
    ## we won't specify this one on the command line,
    ## so it'll fall back to default False
    name = "myFlagArgThatIsNotGivenOnCommandLine"
    print( f'{name} is: ',
        Easy.ArgsParser.GetFlag(name)
    )
    print( Easy.ArgsParser.GetNs("testArg") )

if __name__=='__main__':
    utiltest_ArgParser_01()