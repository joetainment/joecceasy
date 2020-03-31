joecceasy
===========



A Python Module To Make Python Easy
--------------------------------------

This module is an early work in progress, mostly written to be useful for Joe Crawford. It largely exists to make writing Python scripts require less typing, since Joe Crawford has medical issues that prevent much typing.

This module is intentionally and explicitly made to work in ways that are not like idiomatic Python.
  
  
Goals:
========

-Allow easy script like files and one liners that minimize keyboard typing and avoid boilerplate code or reinventing the wheel and are thus able to be used instead of bash scripts or Windows batch scripts, ultimately bringing together the best of both worlds.

-Should allow scripts to avoid manually importing a bunch of modules, they should be available in: Easy.Modules

-Make code easier to read by doing things such as reducing the need for nested parenthesis.

-Provide many easy to reach convenience functions ( as class methods or static methods of primary class).

-Provide easier ways of handling string literals for copying and pasting Windows paths.

-Make it extraordinarily easy to handle arguments and enumerate them.

-Make it extraordinarily easy to do shell like things such as loop through file globs and add dates, suffixes, prefixes to filenames.

-Make it easy to get "command line option" style arguments.

-Make it extremely easy or possibly even default Pythono making scripts run run in their own directory, but should also make easy access to working directory when script was started.

-Have shorthand named functions that just call longer more properly named functions.

-Provide easy cross platform handling of path strings, in particular Windows paths with backsplashes in them that are otherwise hard to handle.

-Should bill itself as a hackish solution it is very practical and solves world problems fast even if it breaks a lot of best practices.

-Be a simpler and more maintainable alternative to forking python itself, in order to provide what is essentially a custom scripting language.

-Provide an '.easypy' script interpreter so that no import lines are even required when executing with the custom interpreter.
 
 
Python problems that motivated creation of this module:
===============================

-One liners are difficult to write and tend to have too many nested parenthesis
-Strings aren't friendly for copy/pasting microsoft windows paths into python code
-Nested parens, nested quotes, etc.
-A pain to call external scripts, sh or bat files.