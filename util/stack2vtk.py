#!/usr/bin/env python2

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

# ------------------------------------------------------------------------

import os
import sys
import numpy as np
import vtk
from pygeo.segyread import SEGYFile

# ------------------------------------------------------------------------
# Settings

AUTHORSHIP = 'Brendan Smithyman, January 2013'
USAGE = '%prog [options] infile'
VERSION = '%prog v1.0\n'
DESCRIPTION = '''
Convert 2D seismic stacks to VTK unstructured grid format.
'''

# ------------------------------------------------------------------------
# Parameter parsing

from optparse import OptionParser

parser = OptionParser(	usage		= USAGE,
			version		= VERSION,
			description	= DESCRIPTION)

parser.add_option('-l', '--label', action='store', dest='label',
		help='label for scalar data')

parser.add_option('-g', '--geom', action='store', dest='geom',
		help='file for geometry information [%default]')

parser.add_option('-s', '--simplify', action='store', dest='simplify',
		help='simplify geometry by sampling every nth, mth [%default]')

parser.add_option('-o', '--override', action='store', dest='override',
		help='override top and bottom elevation [%default]')

parser.set_defaults(	label		= 'Scalars',
			geom		= None,
			simplify	= '1,1',
			override	= None,
)

(options, args) = parser.parse_args()

if (len(args) < 1):
  parser.error('Please specify an input file!')

infile = args[0]

if (len(args) >= 2):
  outfile = args[1]
else:
  outfile = os.path.splitext(infile)[0] + '.vts'

div0, div1 = [int(item) for item in options.simplify.strip().split(',')]

sfdata = SEGYFile(infile)
if (not options.geom is None):
  geomfile = options.geom
  sfgeom = SEGYFile(geomfile)
else:
  geomfile = infile
  sfgeom = sfdata

# ------------------------------------------------------------------------
# Main Program

trh0 = sfgeom.trhead[0]
ntr = sfgeom.ntr
ns = sfgeom.ns

if (ntr != sfdata.ntr or ns != sfdata.ns):
  parser.error('Geometry file and input file must have the same number of samples and traces!')

dz = trh0['dt']/1000.

scalco = float(trh0['scalco'])
if (scalco < 0):
  scalco = -1./scalco

scalel = float(trh0['scalel'])
if (scalel < 0):
  scalel = -1./scalel

traceX = np.array([float(trh['sx'])*scalco for trh in sfgeom.trhead])
traceY = np.array([float(trh['sy'])*scalco for trh in sfgeom.trhead])
traceZ = np.array([float(trh['selev'])*scalel for trh in sfgeom.trhead])

theones = np.ones((ntr,ns))
theslope = -np.arange(ns) * dz
coordarray = np.empty((ntr,ns,3), dtype=np.float64)

coordarray[:,:,0] = (traceX * theones.T).T
coordarray[:,:,1] = (traceY * theones.T).T
if (options.override):
  overtop, overbottom = [float(item) for item in options.override.strip().split(',')]
  depths = np.linspace(overtop, overbottom, ns)
  coordarray[:,:,2] = theones * depths
else:
  coordarray[:,:,2] = (traceZ * theones.T).T + theslope * theones
coordarraysubset = coordarray[::div0,::div1,:]
rcoordarray = coordarraysubset.ravel()

im = sfdata[:]
imsubset = im[::div0,::div1]
imr = imsubset.ravel()
vals = vtk.vtkFloatArray()
vals.SetVoidArray(imr, len(imr), 1)
vals.SetNumberOfComponents(1)
vals.SetName(options.label)

points = vtk.vtkPoints()
darr = vtk.vtkDoubleArray()
darr.SetVoidArray(rcoordarray, len(rcoordarray), 1)
darr.SetNumberOfComponents(3)
points.SetData(darr)

nssub, ntrsub = imsubset.shape

#ipd = vtk.vtkPolyData()
#ipd.SetPoints(points)
#ica = vtk.vtkCellArray()
#ipd.SetPolys(ica)
#ipd.GetPointData().SetScalars(vals)

#delaunay = vtk.vtkDelaunay3D()
#delaunay.SetInput(ipd)
#delaunay.Update()

#writer = vtk.vtkXMLPolyDataWriter()
#writer.SetFileName(outfile)
#writer.SetInput(opd)
#writer.Write()

grid = vtk.vtkStructuredGrid()
grid.SetDimensions(nssub,1,ntrsub)
grid.SetPoints(points)
grid.GetPointData().SetScalars(vals)

writer = vtk.vtkXMLStructuredGridWriter()
writer.SetFileName(outfile)
writer.SetInput(grid)
writer.Write()
