
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

try:
  import pyximport
  pyximport.install()
except:
  print('Cython import failed; pygeo.autopick will not function.')
else:
  try:
    from autopick import *
  except ImportError:
    print('Coud not build/import autopick.pyx; pygeo.autopick will not function.')
    raise
