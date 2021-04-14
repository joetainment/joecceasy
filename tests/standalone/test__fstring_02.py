from joecceasy import Easy

exampleToFormat = "example number is: {number}"
## note that at this point the substitution hasn't happened yet

## now number is defined, late
number = 1


## print while substituting in local variables and capture result...
r = Easy.PrintWithFormat( exampleToFormat, **locals() )

## or, substituting named filed with given value..
r = Easy.PrintWithFormat( exampleToFormat, number=2 )

number = 3
## alternate methods of doing the same, with optional end
r = Easy.PrintWithFormatV( exampleToFormat, kargs=locals(), end='\n\n\n' )

# we don't have to print the results
unprinted = Easy.Format( exampleToFormat, number=4 )
# or
substitutions={ 'number': 5}
unprinted = Easy.FormatV( exampleToFormat, kargs=substitutions )
# or without, keyword arguments
unprinted = Easy.FormatV( exampleToFormat, None, substitutions )


## here are standard python steps
## substituting named filed to print it
## noting wrong with it, but not made particularly
## clear in python documentation
number = 6
resultPyFmt = exampleToFormat.format( **locals() )
print ( f'pure python example: {resultPyFmt}'  )
