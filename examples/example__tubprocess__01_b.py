from joecceasy import Easy

cmd = ["python.exe", "-c", "import time; print(1); time.sleep(1); print(2); time.sleep(1); print(3)" ]
tub  = Easy.Tubprocess( cmd, autoPrint=True )
tub.wait()