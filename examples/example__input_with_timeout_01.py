from joecceasy import Easy


intro = r"""
Easy.Input Example
======================

This script has inputs with timeouts!

Easy.Input is clumsy, only use it for simplest cases.

Behaviour of further calls to Easy.Input, after one of them times out, is awful in terms of user experience. Perhaps use Ascui instead? Or something like whip tail etc.


"""


print( intro, end="")


greeting = Easy.Input( "\n\n"
    + "Please enter a greeting (5 second timeout):",
    5, "Hello"
)
print( f'greeting is: {repr(greeting)}' )


message = Easy.Input(
    "\n\n"
    + "Please enter a message (6 sec timeout):",
    timeout=6,
    default="It's a wonderful world.  :)  "
)
print( f'message is: {repr(message)}' )

