from joecceasy import Easy

def main():
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
    main()