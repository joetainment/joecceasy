from joecceasy.Utils import Funcs
from joecceasy.Utils import see
#from joecceasy import Easy

def test_AnyInAny():
    print('')
    r = Funcs.AnyInAny( ['x','q','z'], ['dog','cat','ferret'])
    assert  r == False  
    r = Funcs.AnyInAny( ['x','q','cats'], ['dog','cat','ferret'])
    assert  r == False
    r = Funcs.AnyInAny( ['x','ca','z'], ['dog','cat','ferret'])
    assert  r == True
    #see('r')
    return r  

def test_AnyEqualsAny():
    print('')
    r = Funcs.AnyEqualsAny( ['x','q','z'], ['dog','cat','ferret'])
    assert  r == False  
    r = Funcs.AnyEqualsAny( ['x','q','ca'], ['dog','cat','ferret'])
    assert  r == False  
    r = Funcs.AnyEqualsAny( ['x','q','cats'], ['dog','cat','x'])
    assert  r == True
    r = Funcs.AnyEqualsAny( ['dog','ca','z'], ['dog','cat','ferret'])
    assert  r == True
    
    r = Funcs.AnyEqualsAny( [1,2,3], [4,5,6])
    assert  r == False
    r = Funcs.AnyEqualsAny( [1,2,3], [4,5,6,2])
    assert  r == True
    #see('r')
    return r  

"""    
def test_b():
    assert True
"""