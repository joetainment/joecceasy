"""
## EasyThread is based on kthread 
## also note that some imports are later is this file, e.g.
#from .Utils import EasyReturnedTimeout


The kthread class itself was modifed slightly to add an exception


kthread license
================

MIT License

Copyright (c) 2019 The Munshi Group

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""




import ctypes
import inspect
#import _thread as thread
import threading

name = "kthread"

def _async_raise(tid, exctype):
    """Raises the exception, causing the thread to exit"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("Invalid thread ID")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble, 
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

class KThread(threading.Thread):
    """Killable thread.  See terminate() for details"""
    def _get_my_tid(self):
        """Determines the instance's thread ID"""
        if not self.is_alive():
            raise threading.ThreadError("Thread is not active")
        
        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id
        
        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
        
        raise AssertionError("Could not determine the thread's ID")
    
    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)
    
    def terminate(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        # WARNING: using terminate(), kill(), or exit() can introduce instability in your programs
        # It is worth noting that terminate() will NOT work if the thread in question is blocked by a syscall (accept(), recv(), etc.)
        try:
          self.raise_exc(SystemExit)
        #
        except RuntimeError as err:
            if not str(err)=='Thread is not active':
                raise

    # alias functions
    def kill(self):
        self.terminate()
        
    def exit(self):
        self.terminate()


########### end of Kthread section

from .Utils import EasyReturnedTimeout

class EasyThread(KThread):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self._return = EasyReturnedTimeout()
        self.killed = False        
    def run(self):
        if self._target is not None:
            self._return = self._target(
                *self._args,
                **self._kwargs
            )
    def join(self, *args, **kargs):
        super().join( *args, **kargs )
        return self._return
    
'''    
    def terminate(self):
        """raises SystemExit in the context of the given thread, which should 
        cause the thread to exit silently (unless caught)"""
        # WARNING: using terminate(), kill(), or exit() can introduce instability in your programs
        # It is worth noting that terminate() will NOT work if the thread in question is blocked by a syscall (accept(), recv(), etc.)
        try:
            super().terminate()
        except RuntimeError as err:
            #if not 
            #print( type(err) )
            if not str(err)=='Thread is not active':
                raise

    # alias functions
    def kill(self):
        self.terminate()
        
    def exit(self):
        self.terminate()    
'''