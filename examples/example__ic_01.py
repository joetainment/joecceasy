from joecceasy import Easy



#ic, tt = Easy.Ic, Easy.TrimAndTab
w = '4'
x = 3
y = 5
z = "some text"

print( """
We can use 'Easy.Ic' directly to show a var, value, and type
\n""")

Easy.Ic(w)


print("""
... but often it's better to make a var pointing to it
with something like  'ic = Easy.Ic'
\n""")

ic=Easy.Ic
ic('y')


print("""
Even better, We can use 'Easy.See' directly
to show a variable by name,
a string evaluated as an expression,
also with value and type
\n""")

Easy.See('y+1')


print("""
again, we could use a shortname instead, e.g.  'see=Easy.See'
\n""")

see=Easy.See
see( 'y + 3')


print( "'Easy.See' can even recursively handle containers of experssions")
print( "Such as lists of tuples or lists of lists")

see(  'y', [ 'x',['z'] ]  )

print("""

'Easy.See' will show the
repr(expression)
rather than the
str(expression)
version of the expression.
""")

lines = "this string\nhas several\nlines!"

see( 'lines',  )


print("""
To show the non repr
str(expression) versions
of the expressions, we can include an integer
at the start of our call to Easy.See (as the first argument)
to add more verbosity
Easy.See( 1, "this expression will be shown with more verbosity" )
This extra verbosity can be very useful for vars
that hold multi line strings etc.
\n""")

see( 1, 'lines')


print("""
Finally, 'Easy.See' will return the value of the first
expression found, and  'Easy.Ic'  will return
the value of the variable it's given!
Note that 'Easy.Ic' will print a poor description
of the vars name if used in complex expreesions.
For anything that's isn't ultra simple,
use  'Easy.See'  not  'Easy.Ic'
\n""")
sum = ic(y)  ## only works in super simple expression
sum += see('y+2')
see( 'sum' )


print("""

'Easy.See' works well even with complex expressions...
""")

product = see('( see("x") *3)-4') * see('y-1+2')
see( 'product' )



## don't do ##  # sum = ic(y) + ic(x)
#print(
"""
Note that 'Easy.Ic' will print a poor description of
the vars name if used in complex expreesions.
'Easy.Ic' is basically a simple knock off of the
'icecream' module in PyPI.
'ic' in icecream does a better job when used in complex lines,
for anything that's isn't ultra simple,
use  'Easy.See'  not  'Easy.Ic'
\n"""
#)
## the following would work quite poorly:
#sum = see('y+2') + ic(y)