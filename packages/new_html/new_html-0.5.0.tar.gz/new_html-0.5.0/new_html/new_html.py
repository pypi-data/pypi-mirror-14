__version__ = "0.5.0"


import sys
from .stuff import Stuff


def new_html():
    print("Executing bootstrap version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    print("Stuff and Boo():\n%s\n%s" % (Stuff, Boo()))
    print "this is new as well"


class Boo(Stuff):
    pass