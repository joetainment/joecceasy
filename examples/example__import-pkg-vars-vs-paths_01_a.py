
"""
This example exists to illustrate how importing submodules in packages works.

On import of qualified pkg.sub.subsub 
  pkg is imported first  into local namespace
    sub is imported into pkg namespace
    subsub is imported into package.subpackage's namespace.
    
    the key to understand is that the submodules are basically
    injected into their parents namespaces, even if their parents
    don't have code that would import them
    
    can imagine some interesting function
"""

def main():
    print( "This is an example of how submodule imports 'inject' into their parent pkgs namespaces" )
    
    print( "importing demoPkgToImport")
    import demoPkgToImport
    print( f"    demoPkg has fake module, \n    is really a namespace, for illustration")
    print( f"  demoPkgToImport.submoduleA type is:\n     {type(demoPkgToImport.submoduleA)}" )
    print( msg1 )
    ## even if the last import hadn't run, the following import would do
    ## the equivalent first prior to importing (injecting) submoduleA
    
    print( "importing demoPkgToImport.submoduleA")
    import demoPkgToImport.submoduleA
    print( f"    demoPkgToImport.submoduleA type is:\n      {type(demoPkgToImport.submoduleA)}\n\n" )
    print( demoPkgToImport.submoduleA )
    print( msg2 )


msg2 = """
so even though demoPkg doesn't itself import submoduleA
submoduleA ends up in demoPkgs namespace
very interesting!
"""

msg1 = """
    at this point, because there's a var, an ns
    in demoPkgToImport, called submoduleA 
"""


if __name__=="__main__":
    main()
