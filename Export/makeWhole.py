###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Import porous unit (2877 spheres) make periodic translations and 
### fuse all together with inlet- and outletzone
###
### Script to load into SALOME v7.6.0
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/adriaan/')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math, numpy 
import SALOMEDS

geompy = geomBuilder.New(theStudy)

Li=200
Rsreal=1.5
part = geompy.ImportBREP('/home/adriaan/corrected_5550.brep' )
[Xmin,Xmax, Ymin,Ymax, Zmin,Zmax] = geompy.BoundingBox(part, True)
Lo=200
Rc = 25.7
Transition = 0
amount = 5550

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Disk_1 = geompy.MakeDiskR(Rc, 2)
inletzone = geompy.MakePrismVecH(Disk_1, OX, Li-Transition, theName='inletzone')
outletzone = geompy.MakePrismVecH(Disk_1, OX, Lo-Transition)
#Transit = geompy.MakePrismVecH(Disk_1, OX, Transition)
#Transit1 = geompy.MakeTranslation(Transit, Li-Transition, 0, 0, theName='Transition1')
#Transit2 = geompy.MakeTranslation(Transit, Li+Lp, 0, 0, theName='Transition2')
#Fuse_1 = geompy.MakeFuseList([inletzone, Transit1], False, False)
[Xmin,Xmax, Ymin,Ymax, Zmin,Zmax] = geompy.BoundingBox(inletzone, True)
part1 = geompy.MakeTranslation(part, Xmax, 0, 0)
#print('fuse inlet')
Fuse_1 = geompy.MakeFuseList([inletzone, part1], False, False)
print('fuse first part')
for i in range (1,1) :
	[Xmin,Xmax, Ymin,Ymax, Zmin,Zmax] = geompy.BoundingBox(Fuse_1, True)
	Translation = geompy.MakeTranslation(part, Xmax, 0, 0)
	#parts.append(Translation)
	print('Translation ' + str(i))
	Fuse_1 = geompy.MakeFuseList([Fuse_1, Translation], False, False)
	print('Fuse ' + str(i))
	geompy.ExportBREP(Fuse_1, '/home/adriaan/Export/fluid_Whole'+str(2*Rsreal)+'mm.brep' )
	print('ExportBREP')
#Fuse_1 = geompy.MakeFuseList([Fuse_1, Transit2], False, False)
#print('fuse transit')
[Xmin,Xmax, Ymin,Ymax, Zmin,Zmax] = geompy.BoundingBox(Fuse_1, True)
outletzone = geompy.MakeTranslation(outletzone, Xmax, 0, 0, theName='outletzone')
Fuse_1 = geompy.MakeFuseList([Fuse_1, outletzone], False, False)
print('fuse outlet')
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( part, 'part' )
geompy.addToStudy( Fuse_1, 'fluidAroundPacking' )

geompy.ExportBREP(Fuse_1, '/home/adriaan/Export/fluid_'+str(amount)+'_'+str(2*Rsreal)+'mm.brep' )
print('ExportBREP')

# Set HDF file path
#path='/home/adriaan/Export/Unstructured_Whole_'+str(Rsreal*2)+'mm.hdf'
# Save the study
#salome.myStudyManager.SaveAs(path,salome.myStudy,False)

import os
from killSalomeWithPort import killMyPort
killMyPort(os.getenv('NSPORT'))

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
