###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Import sphere coordinates of packing from Yade and define fluid domain by cutting out spheres 
###
### Script to load into SALOME v7.6.0
###

import sys
import salome
import numpy

salome.salome_init()
theStudy = salome.myStudy

#import salome_notebook
#notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/adriaan')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

#parameters
Rc=51.4/2
Rsreal=1.5
scaleFactor = 1
Rs=scaleFactor*Rsreal
#Transition from structured mesh to position of sphere (not too abrupt)
Transition = 25

#Loading centres
data = numpy.loadtxt('spheres2797')

maxi = 0
mini = 100 
for index in range (0,len(data)) :
	if data[index][0] > maxi : 
		maxi = data[index][0]
	if data[index][0] < mini :
                mini = data[index][0]
print(mini)
print(maxi)
Lptot = maxi+2*Rs-mini
Li=25
Lo=25
frac = 1
part=1
Lp = Lptot*frac
print(str(Lp))

geompy = geomBuilder.New(salome.myStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Disk_1 = geompy.MakeDiskR(Rc, 2)
tube = geompy.MakePrismVecH(Disk_1, OX, Li+Lp+Lo)
#tube = geompy.MakeTranslation(tube, Li+(part-1)*Lp, 0, 0)

fluid = tube
#Enable to import BREP and continu a (crashed) operation
fluid = geompy.ImportBREP('/home/adriaan/Export/build1_2797_500_3.0mm.brep' )
notadded = []
volume_spheres = 0
volume_spheres_wanted = 0
#Set 1 to have only gaps
onlyGaps = 0
tried = 0
#Add loop to add all spheres
for index in range (501,len(data)) :	
	if tried < 20 and data[index][0]<14+1.65:
		x = data[index][0]+Li
		y = data[index][1]
		z = data[index][2]
		radius = data[index][3]
		p = geompy.MakeVertex(x,y,z)
		try :
			sphere = geompy.MakeSpherePntR(p, radius)
		except :
			print('Failed making sphere')
			pass
		try:
			fluid = geompy.MakeCut(fluid, sphere, True)
		except:
			print('step ' + str(index) + ' added to notadded')		
			notadded.append(sphere)
			tried = tried +1
			try:
				fluid = geompy.ProcessShape(fluid, ["FixShape"], ["FixShape.Tolerance3d", "FixShape.MaxTolerance3d"], ["1e-07", "1"])
			except:
				print('Processing shape failed')
			else:
				print('Processing shape succeeded')
			pass
		else:
			#run block if try succeeded (no exception occured)
			sphere.UnRegister()
			print('step ' + str(index))
			if index%500 == 0 :
				geompy.ExportBREP(fluid, '/home/adriaan/Export/build1_'+str(len(data))+'_'+str(index)+'_'+str(2*Rsreal)+'mm.brep' )
geompy.ExportBREP(fluid, '/home/adriaan/Export/build1_'+str(len(data))+'_'+str(Lp)+'_3mm.brep' )

import os
from killSalomeWithPort import killMyPort
killMyPort(os.getenv('NSPORT'))
