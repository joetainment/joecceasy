from joecceasy import Easy

if True:
    trimmed = Easy.TrimAndTab( r"""
        ## first non whitespace must be "#", this line gets removed and others unindented to match
        Here's some trimmed lines,
        trimmed lines are really useful.
        The literal code has nice indentation.
        Code is easier to copy/paste and it's easier to write big strings
        inside in functions/classes.
        They can end (from a practical perspective)
        with windows backslashes too!
        eg.
        C:\Windows\
    """)
    
print( trimmed )
