import sys

if sys.version_info < (3,0):
    from py2 import *
else:
    from pybagel.py3 import *