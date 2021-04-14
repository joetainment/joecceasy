from joecceasy import Easy

cmd= ["python.exe", "-c", "import time; print(1); time.sleep(1); print(2)" ]
tub  = Easy.Tubprocess( cmd )
for i in tub:
    print( i.out, end='' )
