joecceasy
===========



A Python Module To Make Python Easy
--------------------------------------

This module is an early work in progress, mostly written to be useful for Joe Crawford. It largely exists to make writing Python scripts require less typing, since Joe Crawford has medical issues that prevent much typing. (Much of joecceasy was in fact written using voice recognition.)

This module is intentionally and explicitly made to work in ways that are not like idiomatic Python. It is purposefully "hack'ish" and it prioritizes practicality over any kind of code purity. It helps the user "get the job done" by trading some elegance for practical shortcuts.

However, the module also attempts not to interfere with regular Python programming unless you explicitly enable such features. Users should be able to use as few or as many of joecceasy's features as they like.

Code can use no magic...

```python
from joecceasy import Easy
print( Easy.Args )
```

...or, lot's of magic...

```
from joecceasy import Easy; exec(Easy.Magic); exit(); #%exit
######## everything after the #%exit line is run through/via the magic

## You can easily make system/shell calls with much more literal syntax
#%call echo This is a magic comment that calls the system's/shell's echo function.

## see more examples of magic in the examples section of this readme.
```

.. or, even more magic, by launching the script with a custom interpreter ...

```
#%call echo If we use a special interpreter to run the script
#%call echo we don't even need import lines or other boilerplate code.
#%call echo Finally, python-based scripts as short as bash or batch scripts!
```

  
  
Goals:
========

- Allow easy script like files and one liners that minimize keyboard typing and avoid boilerplate code or reinventing the wheel and are thus able to be used instead of bash scripts or Windows batch scripts, ultimately bringing together the best of both worlds.

- Should allow scripts to avoid manually importing a bunch of modules, they should be available in: Easy.Modules

- Make code easier to read by doing things such as reducing the need for nested parenthesis.

- Provide many easy to reach convenience functions ( as class methods or static methods of primary class).

- Provide easier ways of handling string literals for copying and pasting Windows paths.

- Make it extraordinarily easy to handle arguments and enumerate them.

- Make it extraordinarily easy to do shell like things such as loop through file globs and add dates, suffixes, prefixes to filenames.

- Make it easy to get "command line option" style arguments.

- Make it extremely easy or possibly even default Pythono making scripts run run in their own directory, but should also make easy access to working directory when script was started.

- Have shorthand named functions that just call longer more properly named functions.

- Provide easy cross platform handling of path strings, in particular Windows paths with backsplashes in them that are otherwise hard to handle.

- Should bill itself as a hackish solution it is very practical and solves world problems fast even if it breaks a lot of best practices.

- Be a simpler and more maintainable alternative to forking python itself, in order to provide what is essentially a custom scripting language.

- Provide an '.easypy' script interpreter so that no import lines are even required when executing with the custom interpreter.
 
 
Python problems that motivated creation of this module:
===============================

- One liners are difficult to write and tend to have too many nested parenthesis

- Strings aren't friendly for copy/pasting microsoft windows paths into python code

- Nested parens, nested quotes, etc.

- A pain to call external scripts, sh or bat files.

  
  
  

More Examples
==============


Various uses of Magic
---------------
```
from joecceasy import Easy; exec(Easy.Magic); exit(); #%exit
######## everything after the #%exit line is run through the magic

#### Here's some examples of magic/easy things:

## You can easily make system/shell calls with much more literal syntax
## that is friendly to copy/pasting paths

#%call echo This is a magic comment that calls the system's/shell's echo function.

## You can do variable substitution as well:
msg = "Here's a substituted message."
#%call echo #%msg%#

#%callq echo This is a magic comment that quiet calls the echo function.
## The quiet call won't be output directly, but it is captured.
o = tmpReturned.stdout
print( f"Captured output was: {tmpReturned.stdout}" )

## All modules are available without importing, and are lazy loaded as required:
cwdStr = Easy.Mods.os.getcwd()
print( f"Current working directory is: {cwdStr}" )
```

Easy.TrimAndTab
---------------

```
from joecceasy import Easy
if 'code block'!='has indentation':
    msg1 = Easy.TrimAndTab( r"""
        ## Indentation Marker
        This text will be unindented, allowing multiline
        strings to fit nicely into code blocks.
        
        Here's a windows path, with backslashes,
        copy and pasted without concerns about it
        ending with a backslash:
    """)
    msg2 = Easy.TrimAndTab( r"""
        ##
        C:\Users\Public\
    """)
    print( msg1 )
    print( msg2 )
    msg3 = Easy.TrimAndTab( r"""
        ###
        These sorts of tricks make dealing with windows paths
        much less error prone, all while keeping all code,
        even the string parts, indented fully inside the block.
    """)
    print( msg3 )
```