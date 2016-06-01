###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Import whole geometry, define boundary faces and create unstructured mesh 
###
### Script to load into SALOME v7.6.0
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/adriaan/Export')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math, numpy
import SALOMEDS

geompy = geomBuilder.New(theStudy)

#parameters
Li=200
amount = 5755
Rsreal = 1.5
#Checking Lp
data = numpy.loadtxt('/home/adriaan/spheres2797')
maxi = 0
for index in range (0,len(data)) :
        if data[index][0] > maxi :
                maxi = data[index][0]
Lpi = maxi*1000 + Rsreal
#amount of periodic porous units (parts)
aparts = 1
Lp=aparts*Lpi
Lo=200
Rc = 25.7
Transition = 25

#packedTube = geompy.ImportBREP('/home/adriaan/Export/gap_'+str(amount)+'_'+str(2*Rsreal)+'mm.brep', theName='packedTube' )
#packedTube = geompy.ImportBREP('/home/adriaan/Export/fluid_CombinedScale_ProcessShape_2877_2876_3000.0mm.brep', theName='packedTube' )
packedTube = geompy.ImportBREP('/home/adriaan/Export/fluid_2797_3.0mm.brep')

#Calculation of real porosity
amountOfSpheres = geompy.MakeVertex(0,0,0)
geompy.addToStudy(amountOfSpheres, 'amountOfSpheres='+str(amount))
volume_packedzone = Lp*math.pi*Rc**2
volumes = amount*1.3333333333333333333*math.pi*Rsreal**3
epsWanted = 1-volumes/volume_packedzone
epsilonWanted = geompy.MakeVertex(0,0,0)
#geompy.addToStudy(epsilonWanted, 'epsilonWanted='+str(epsWanted))
epsilonAchieved = geompy.MakeVertex(0,0,0)
volume_inletoutletzone = (Li+Lo+2*Transition)*math.pi*Rc**2
volume_fluidAroundPacking = geompy.BasicProperties(packedTube)[2]-volume_inletoutletzone
epsAchieved = volume_fluidAroundPacking/volume_packedzone
geompy.addToStudy(epsilonAchieved, 'epsilonAchieved='+str(epsAchieved))

# CREATE GROUPS FACES

#INLET/OUTLET
inletFaces = []
outletFaces = []
#If you loop on interestion: error: Multiple faces near the given point are found
#inner loop starts at 30 degrees and turns 60 degrees
left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( 0, 0, 0))
inletFaces.append(left)
right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+2*Lo, 0, 0 ))
outletFaces.append(right)

#CREATE GROUPS VOLUMES
#inletShapes = []
#outletShapes = []
#midShapes = []
#inner loop starts at 30 degrees and turns 60 degrees
#left  = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( 0, 0, 0 ))
#inletShapes.append(left)
#right = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0, 0 ))
#outletShapes.append(right)
#middle = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( Li+Transition+Lp/2, 0, 0 ))
#midShapes.append(middle)

#WALLS
inletWalls = []
outletWalls = []
porousWalls = []
internals = []
left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li-Transition, 0, 0))
internals.append(left)
right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition, 0, 0 ))
internals.append(right)
wall  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex(Li/2, Rc, Rc ))
inletWalls.append(wall)
wall  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex(Li+Lp+Lo/2, Rc, Rc ))
outletWalls.append(wall)
for i in range (0,aparts) : 
	wall  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex(Li+i*Lpi+0.01*Rsreal, Rc, Rc ))
	porousWalls.append(wall)
	internal  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex(Li+i*Lpi, Rc, Rc ))
	internals.append(internal)

#Add groups to Study
#volumes
#inletzone = geompy.CreateGroup( packedTube, geompy.ShapeType["SOLID"], "inletzone" )
#geompy.UnionList( inletzone, inletShapes)
#outletzone = geompy.CreateGroup( packedTube, geompy.ShapeType["SOLID"], "outletzone" )
#geompy.UnionList( outletzone, outletShapes)
#porouszone = geompy.CreateGroup( packedTube, geompy.ShapeType["SOLID"], "porouszone" )
#geompy.UnionList( porouszone, midShapes)

#faces
all = geompy.SubShapeAll( packedTube, geompy.ShapeType["FACE"])
inlet = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "inlet" )
geompy.UnionList( inlet, inletFaces)
outlet = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "outlet" )
geompy.UnionList( outlet, outletFaces)
inletWall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "inletWall" )
geompy.UnionList( inletWall, inletWalls)
outletWall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "outletWall")
geompy.UnionList( outletWall, outletWalls)
porousWall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "porousWall" )
geompy.UnionList( porousWall, porousWalls)
sphereSurfaces = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "sphereSurfaces")
geompy.UnionList( sphereSurfaces, all )
geompy.DifferenceList( sphereSurfaces, inletFaces + outletFaces + inletWalls + outletWalls + internals + porousWalls)

print ("saving hdf")
try:
   # Save the study
   salome.myStudyManager.SaveAs(r'/home/adriaan/Export/Mesh_PackedBed_Total_'+str(amount)+'_'+str(2*Rsreal)+'mm.hdf',salome.myStudy,False)
except:
   print 'Saving .hdf failed. Invalid file name?'

###
### SMESH component
###

print("starting mesh")

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New(theStudy)
Mesh_1 = smesh.Mesh(packedTube)
NETGEN_2D3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
NETGEN_3D_Parameters = NETGEN_2D3D.Parameters()
#NETGEN_3D_Parameters.SetMaxSize( 0.5 )
#NETGEN_3D_Parameters.SetMinSize( 0.000674977 )
NETGEN_3D_Parameters.SetMaxSize( 5 )
NETGEN_3D_Parameters.SetMinSize( 0.5 )
#NETGEN_3D_Parameters.SetMinSize( 0.01 )
NETGEN_3D_Parameters.SetSecondOrder( 0 )
NETGEN_3D_Parameters.SetOptimize( 1 )
NETGEN_3D_Parameters.SetFineness( 2 )
NETGEN_3D_Parameters.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters.SetFuseEdges( 1 )
NETGEN_3D_Parameters.SetQuadAllowed( 0 )
isDone = Mesh_1.Compute()

inlet_1 = Mesh_1.GroupOnGeom(inlet,'inlet',SMESH.FACE)
outlet_1 = Mesh_1.GroupOnGeom(outlet,'outlet',SMESH.FACE)
sphereSurfaces_1 = Mesh_1.GroupOnGeom(sphereSurfaces,'sphereSurfaces',SMESH.FACE)
inletWall_1 = Mesh_1.GroupOnGeom(inletWall,'inletWall',SMESH.FACE)
outletWall_1 = Mesh_1.GroupOnGeom(outletWall,'outletWall',SMESH.FACE)
porousWall_1 = Mesh_1.GroupOnGeom(porousWall,'porousWall',SMESH.FACE)
#inletzone_1 = Mesh_1.GroupOnGeom(inletzone,'inletzone',SMESH.VOLUME)
#outletzone_1 = Mesh_1.GroupOnGeom(outletzone,'outletzone',SMESH.VOLUME)
#porouszone_1 = Mesh_1.GroupOnGeom(porouszone,'porouszone',SMESH.VOLUME)

## Set names of Mesh objects
smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
smesh.SetName(NETGEN_3D_Parameters, 'NETGEN 3D Parameters')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(outlet_1, 'outlet')
smesh.SetName(inlet_1, 'inlet')
smesh.SetName(inletWall_1, 'inletWall')
smesh.SetName(outletWall_1, 'outletWall')
smesh.SetName(porousWall_1, 'porousWall')
smesh.SetName(sphereSurfaces_1, 'sphereSurfaces')
#smesh.SetName(inletzone_1, 'inletzone')
#smesh.SetName(outletzone_1, 'outletzone')
#smesh.SetName(porouszone_1, 'porouszone')

print("meshing completed")

try:
  Mesh_1.ExportUNV( r'/home/adriaan/Export/Mesh_Coarse'+str(amount)+'_'+str(2*Rsreal)+'mm.unv' )
except:
  print 'ExportUNV() failed. Invalid file name?'

print ("saving hdf")
try:
   # Save the study
   salome.myStudyManager.SaveAs(r'/home/adriaan/Export/Mesh_PackedBed_Total_'+str(amount)+'_'+str(2*Rsreal)+'mm.hdf',salome.myStudy,False)
except:
   print 'Saving .hdf failed. Invalid file name?'

import os
from killSalomeWithPort import killMyPort
killMyPort(os.getenv('NSPORT'))
