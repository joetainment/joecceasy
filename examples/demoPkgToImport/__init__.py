## this is __init__.py
 
#submoduleA = '''this is defined in "__init__.py"'''
import types
submoduleA = types.SimpleNamespace( a = "this var is declared in __init__.py of demoPkg")
print( "    demoPkg init ran" )