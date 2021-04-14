from joecceasy import Easy

        
#tub = Easy.Tubprocess( ["python.exe", "example__func__PrintLoop__01_a.py"], ) #errToOut=True )

for i in Easy.Tubprocess( ["python.exe", "-c", "import time; print(1); time.sleep(1); print(2); time.sleep(1); print(3)" ]):
    print( i.out, end='' )
exit()

    

for i, (out, err), in enumerate(tub):
    print( out, end='' )
    #print( err, end='' )
    if i > 80:
        break
    
print('break')
print( tub.outStr )
Easy.Mods.time.sleep(1.5)
print( "next" )
print( tub.next().out )
print( "resuming" )

for out, err2 in tub:
    print( out, end='' )
    print( err2, end='' )

print( tub.outStr[-25:] )