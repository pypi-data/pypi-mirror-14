from __future__ import absolute_import, division, print_function, unicode_literals
from sys import argv
from os.path import isfile
import pymash

if len(argv) > 1 and isfile(argv[1]):
    print ('pymash version {0}.{1}'.format(*pymash.pymash_version))
    print ('using ', argv[1])
    print()
    pymash.mash(argv[1])

else:
    print ("""Usage:
    Run python -m [PATH TO CFG FILE]
    """)
