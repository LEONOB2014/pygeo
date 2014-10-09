
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

'''
.. module:: pygeo.segyread
   :platform: Unix
   :synopsis: Provides an interface for interacting with SEG-Y files.

.. moduleauthor:: Brendan Smithyman <bsmithyman@eos.ubc.ca>

'''

try:
  import pyximport
  pyximport.install()
except:
  print('Cython import failed; pygeo.segyread will use the legacy (pure Python) mode.')
  from segyreadvanilla import *
else:
  try:
    from segyread import SEGYFile
  except ImportError:
    print('Could not build/import segyread.pyx; pygeo.segyread will use the legacy (pure Python) mode.')
    from segyreadvanilla import SEGYFile
