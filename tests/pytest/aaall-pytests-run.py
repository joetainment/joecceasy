#!/usr/bin/env python
import os,   pytest
import pytest

results = pytest.main(  [
    '--verbose',
    '--capture', 'tee-sys',
    os.path.dirname(__file__),
]  )

"""    
with open('gitignore----aaall-pytests-output.txt','w') as fh:
    fh.write( 'hello' )

print( 'results: ', results )
print( dir(pytest) )
"""bb
that bvbvbavba<