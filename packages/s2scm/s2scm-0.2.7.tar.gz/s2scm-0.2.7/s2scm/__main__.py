import sys
from project import *

def usage(status = 0):
    print 'Usage: s2scm infile.scm outfile.sb2'
    sys.exit(status)

if '-h' in sys.argv or '-?' in sys.argv or '--help' in sys.argv:
    usage()
elif '-v' in sys.argv or '--version' in sys.argv:
    print '''s2scm version 0.2.7

Copyright (C) 2016 Jeandre Kruger.

s2scm is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

s2scm is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with s2scm.  If not, see <http://www.gnu.org/licenses/>.'''
    sys.exit(0)

if len(sys.argv) != 3:
    usage(1)

compile_project(sys.argv[1], sys.argv[2])
