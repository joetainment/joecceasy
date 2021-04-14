from joecceasy import Easy

exampleToFormat = "example number is: {number}"
## note that at this point the substitution hasn't happened yet

## now number is defined, late
number = 1

## now we want to use our number, late
result = eval( Easy.Fstring( exampleToFormat ) )
print(result)


## here's a pure Python example
number = 2
resultPyFmt = exampleToFormat.format( **locals() )
print ( f'pure python example: {resultPyFmt}'  )

