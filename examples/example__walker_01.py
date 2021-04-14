from joecceasy import Easy

def main():
    
    paths = ['..','.']
    absOfEntries = [ i.abs for i in Easy.WalkAnIter(paths)  ]
    for i in absOfEntries:
        print( i )
    
if __name__=='__main__':
    main()
    
    
"""
def main(maxEntries = 99):
    i = -1
    print( "Walker test, Walking current directory:" )
    for entry in Easy.WalkAnIter( ['.'] ):
        i += 1 ## because i start at -1, 1st run of line will be 0
        if i > maxEntries:
            break
        print(entry.abs)
    print( ' \n ' )
"""

#isFileByPython = os.path.isfile(entry.abs)
#    print( 'entry: ', entry.name, 'f', entry.isFile, 'd', entry.isDir,
#           'fa', entry.isFileAt, 'da', entry.isDirAt, 'pf', isFileByPython, se#p='  ')
#end='' )
#print( entry.abs, entry.isFileAt, entry.isDirAt, sep=' ' )
#print( entry.__dict__ )