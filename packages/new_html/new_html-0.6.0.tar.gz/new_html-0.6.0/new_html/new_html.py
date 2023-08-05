__version__ = "0.6.0"


import sys
from .stuff import Stuff


def new_html():
    print("Executing new_html version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    print "this is new as well"


class Boo(Stuff):
    pass