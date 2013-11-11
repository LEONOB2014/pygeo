#!/usr/bin/env python

# pygeo - a distribution of tools for managing geophysical data
# Copyright (C) 2011, 2012 Brendan Smithyman

# This file is part of pygeo.

# pygeo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.

# pygeo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with pygeo.  If not, see <http://www.gnu.org/licenses/>.

# ----------------------------------------------------------------------

from optparse import OptionParser
import os.path
from pygeo.segyread import SEGYFile

usage = 'usage: %prog [options] infile [outfile]'
version = '\n%prog v1.0\nBrendan Smithyman\nJuly, 2011'
parser = OptionParser(usage=usage, version=version)
parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                  help='display status information')
parser.add_option('-n', '--normalize', action='store_true', dest='normalize',
                  help='normalize each trace to unit amplitude')
parser.set_defaults(verbose=False, normalize=False)
(options, args) = parser.parse_args()

if (len(args) != 1 ):
  parser.error('Please specify a valid filename to convert.')
elif (not os.path.isfile(args[0])):
  parser.error('File %s does not exist!'%(args[0],))

infile = args[0]

if (len(args) > 1):
  outfile = args[1]
else:
  outfile = infile + '.su'

if (options.verbose):
  print('\nSEG-Y --> SU File Converter v1.0\nBrendan Smithyman, July 2011\n\n\tConverting \'%s\' to \'%s\'...\n'%(infile, outfile))

sf = SEGYFile(infile, verbose=options.verbose, majorheadersonly=False)
intr = sf.readTraces()
if (options.normalize):
  intr = sf.sNormalize(intr)

if (options.verbose):
  print('Generating output file.')

if (len(intr.shape) == 1):
    intr = [intr]

sf.writeSU(outfile, intr, sf.trhead)

if (options.verbose):
  print('Done!\n')

