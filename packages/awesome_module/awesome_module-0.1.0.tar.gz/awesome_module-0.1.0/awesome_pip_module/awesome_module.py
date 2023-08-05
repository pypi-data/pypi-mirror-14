__version__ = "0.1.0"

import sys

def awesome_module():
   print("Executing awesome_module version %s." % __version__)
   print("List of argument strings: %s" % sys.argv[1:])
   print "this is new as well"

# awesome_module [yes, no, yes]