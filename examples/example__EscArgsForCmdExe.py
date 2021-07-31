from joecceasy import Easy
spc = ' '


echoCmdAndArgs = [ r'''echo''', r'''test!''', r'''another>test''', r'''test three''', r'''c:\some dir\file.txt''' ]
echoCmdAndArgs = Easy.EscArgsForWin( echoCmdAndArgs )
print( "esc: ", echoCmdAndArgs )
Easy.CallInteractive( echoCmdAndArgs, loud=True )


pyCmdAndArgs = [ r'''python''', r'''-c''', r'''import sys; print( sys.argv[0] ); print( len(sys.argv) ); print('hello you'); print( "hello again")''' ]
pyCmdAndArgs = Easy.EscArgsForCmdExe( pyCmdAndArgs )
print( "esc: ", pyCmdAndArgs )
Easy.CallInteractive( pyCmdAndArgs, loud=True )
