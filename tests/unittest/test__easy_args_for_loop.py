#!/usr/bin/env python3

import unittest

def easy_args_for_loop():
    from joecceasy import Easy; Easy.Init( shouldAutoLoadCode=False )

    ## Easy.ArgsE and Easy.Args give us easy access to our programs arguments,
    ## while conveniently not including zero sys.argv[0]
    ## (argument zero) this way we can easily process
    ## just the arguments given to this script.

    for i, arg in Easy.ArgsE:
        print( f"arg at index {i}  (at sys.argv index {i+1}) : {arg}" )


    ## Same as the function call, Easy.EnumArgs()
    #for i, arg in Easy.EnumArgs():
    #    print( f"arg at index {i}: in sys index {i+1} : {arg}" )

    ## or, if we didn't want to bother enumerating them:
    #for arg in Easy.Args:
    #    print( f"Easy.Args contains: {arg}" )    

    if Easy.ArgsCount < 1:
        print( Easy.TrimAndTab(r"""
            ###
            No arguments given.
            Please provide at least one argument.
            For example:
            By dragging and dropping a file onto this script.
        """))


class TestEasyArgsForLoop(unittest.TestCase):
    def test_easy_args_for_loop(self):
        r = easy_args_for_loop()
        ## Example, here we could check something
        self.assertEqual(  r, r )  ## todo - put something else here
        ## Example, here we make sure an error gets raised
        ## the error type we're looing for goes in the parens
        with self.assertRaises(AssertionError): ## todo - use different type
            assert(False) ## todo - actually generate specific error
    
if __name__ == '__main__':
    unittest.main()
