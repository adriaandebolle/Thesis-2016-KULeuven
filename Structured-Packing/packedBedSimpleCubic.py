# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v7.6.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/adriaan')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

#parameters
Rc=0.0514/2
Rs=0.005/2
Li=0.2
Lp=0.304
Lo=0.2
#Transition from structured mesh to position of sphere (not too abrupt)
Transition = 0.015
#number of loop steps to have enough spheres 
lengthSteps = int(Lp//(2*Rs))
otherSteps = int((2*Rc)//(2*Rs))

geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Divided_Disk_1 = geompy.MakeDividedDisk(Rc, 2, GEOM.HEXAGON)
inletzone = geompy.MakePrismVecH(Divided_Disk_1, OX, Li-Transition)
Extrusion_1 = geompy.MakePrismVecH(Divided_Disk_1, OX, Lp+2*Transition)
packedzone = geompy.MakeTranslation(Extrusion_1, Li-Transition, 0, 0)
#Circle_1 = geompy.MakeCircle(None, OX, Rc)
#inlet = geompy.MakeFaceWires([Circle_1], 1)
#Extrusion_1 = geompy.MakePrismVecH(inlet, OX, Lp)
#packedzone = geompy.MakeTranslation(Extrusion_1, Li, 0, 0)
outletzone = geompy.MakeTranslation(inletzone, Li+Lp+Transition, 0, 0)
#Vertex_1 = geompy.MakeVertex(Li+Rs, 0, 0)
#Sphere_1 = geompy.MakeSpherePntR(Vertex_1, Rs)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( inletzone, 'inletzone' )
geompy.addToStudy( packedzone, 'packedzone' )
geompy.addToStudy( outletzone, 'outletzone' )

# adding all spheres in an array 
# centres can be used for extra calculations like finding faces closest to sphere centre (Sphere surface)
centres = []
spheres = []

#range (3,5) gives 3 and 4; so end in not included
#Because of adding space between spheres: lengthStep (Otherwise sphere outside zone)
#Removing spheres outside of packedZone: otherSteps +2 for beginning because beginning is included and -1 for end point
#adapted steps is not necessary because of if-test
#Add loop to add all spheres
for i in range (2,3) :
    for k in range (-otherSteps+2, otherSteps-1) :
	for l in range (-otherSteps+2, otherSteps-1) :
		#Meshing problem: solved by adding 2% of Rs space between adjacent spheres
		#coordinates of new sphere
		x = Li+i*2.01*Rs
		y = k*2.01*Rs
		z = l*2.01*Rs
		#Don't make the sphere if it will be outside the tube
		#distance from tube centre to new sphere centre:
		centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
		if centreToCentre < Rc-Rs :
	  		#Translation = geompy.MakeTranslation(Sphere_1,i*2*Rs+0.01*Rs,k*2*Rs+0.01*Rs,l*2*Rs+0.01*Rs)
			p = geompy.MakeVertex(x,y,z)
			sphere = geompy.MakeSpherePntR(p, Rs)
			geompy.addToStudy(sphere, 'p'+str(i)+str(k)+str(l))
      			spheres.append( sphere )
      			centres.append( p )
	pass
    pass
pass

######
#This part is not necessary
#Make a partition of all spheres
#spheresXYZ = geompy.MakePartition(spheres,[], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
#geompy.addToStudy( spheresXYZ, 'spheresXYZ' )
#fluid = geompy.MakeCutList(packedzone, [spheres], True)
######

#Calculation of real porosity
amountOfSpheres = geompy.MakeVertex(0,0,0)
geompy.addToStudy(amountOfSpheres, 'amountOfSpheres='+str(len(spheres)))
volumep = Lp*math.pi*Rc**2
volumes = len(spheres)*4/3*math.pi*Rs**3
eps = 1-volumes/volumep
epsilon = geompy.MakeVertex(0,0,0)
geompy.addToStudy(epsilon, 'epsilon='+str(eps))

#Making cut to have fluid around packing in porous zone
fluid = geompy.MakeCutList(packedzone, spheres)
geompy.addToStudy(fluid, 'fluidAroundPacking')
packedTube = geompy.MakePartition([inletzone, outletzone, fluid], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)
geompy.addToStudy(packedTube, 'packedTube')

# CREATE GROUPS FACES

###
#Several faces when divided disk is used
#sphFaces = []
#for p in centres:
#  sph = geompy.GetFaceNearPoint( packedTube, p )
#  sphFaces.append( sph )
###

#INLET/OUTLET
inletFaces = []
outletFaces = []
poroInletFaces = []
poroOutletFaces = []
#If you loop on interestion: error: Multiple faces near the given point are found
#inner loop starts at 30 degrees and turns 60 degrees
for x in [0.5,1.5,2.5,3.5,4.5,5.5] :
	left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( 0, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	inletFaces.append(left)
	right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	outletFaces.append(right)
	poroleft  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li-Transition, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	poroInletFaces.append(poroleft)
	pororight = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	poroOutletFaces.append(pororight)
#outer loop starts at 15 degrees and turns 30 degrees
for x in [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75,5.25,5.75] :
	left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( 0, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	inletFaces.append(left)
	right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	outletFaces.append(right)
	poroleft  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li-Transition, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	poroInletFaces.append(poroleft)
	pororight = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	poroOutletFaces.append(pororight)

#WALLS
inletWalls = []
poroWalls = []
outletWalls = []
#wall loop starts at 15 degrees and turns 30 degrees (same as outer inlet/outlet loop)
for x in [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75,5.25,5.75] :
	wallinlet  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Rs, Rc*math.cos(x*math.pi/3), Rc*math.sin(x*math.pi/3) ))
	inletWalls.append(wallinlet)
	wallporo  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+0.1*Rs, Rc*math.cos(x*math.pi/3), Rc*math.sin(x*math.pi/3) ))
	poroWalls.append(wallporo)
	walloutlet = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo-0.01*Rs, Rc*math.cos(x*math.pi/3), Rc*math.sin(x*math.pi/3) ))
	outletWalls.append(walloutlet)

#INTERNAL FACES 
internal = []
pinternal1 = []
pinternal2 = []
pinternal3 = []
test = []
#rotor shape: -X- (6 faces)
for x in [0,1,2,3,4,5] :
	left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( 0.5*Li, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	internal.append(left)
	test.append(left)
	right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+0.5*Lo, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	internal.append(right)
	poro = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition/2, 0.1*Rc*math.cos(x*math.pi/3), 0.1*Rc*math.sin(x*math.pi/3) ))
	pinternal1.append(poro)
#perpendicular on hexagonals
for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5] :
	left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Rs, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	internal.append(left)
	right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo-0.01*Rs, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	internal.append(right)
	poro = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition/2, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	pinternal2.append(poro)
#hexagonals
#getcoordinates: python console: study = salome.myStudy; object = study.FindObject(Vertex); vert = object.GetObject(); coord = geompy.PointCoordinates(vert); print coord
#Study of divided disk gave 60.34% of Rc to get faces
for x in [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75,5.25,5.75] :
	left  = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Rs, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	internal.append(left)
	right = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo-Rs, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	internal.append(right)
	poro = geompy.GetFaceNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition/2, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	pinternal3.append(poro)

#CREATE GROUPS VOLUMES
inletShapes = []
outletShapes = []
#inner loop starts at 30 degrees and turns 60 degrees
for x in [0.5,1.5,2.5,3.5,4.5,5.5] :
	left  = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( 0, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	inletShapes.append(left)
	right = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	outletShapes.append(right)
#outer loop starts at 15 degrees and turns 30 degrees
for x in [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75,5.25,5.75] :
	left  = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( 0, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	inletShapes.append(left)
	right = geompy.GetBlockNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0.95*Rc*math.cos(x*math.pi/3), 0.95*Rc*math.sin(x*math.pi/3) ))
	outletShapes.append(right)

#CREATE GROUPS EDGES (for meshing)
walledges = []
walledgesporo = []
inversedwalledges = []
inversedwalledgesporo = []
xinlet = []
xporo = []
xoutlet = []
innerandrings = []
innerandringsporo = []

#outer loop starts at 0 degrees and turns 30 degrees
for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5] :
	#xedges
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( Li/2, Rc*math.cos(x*math.pi/3), Rc*math.sin(x*math.pi/3) ))
	xinlet.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Lo/2,Rc*math.cos(x*math.pi/3),Rc*math.sin(x*math.pi/3)))
	xoutlet.append(right)
	left  = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li/2, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	xinlet.append(left)
	right = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo/2, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	xoutlet.append(right)
	poro = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition/2, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	xporo.append(poro)
	poro = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex(Li+Lp+Transition/2,Rc*math.cos(x*math.pi/3),Rc*math.sin(x*math.pi/3) ))
	xporo.append(poro)
for x in [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5] :
	#inner walledges
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( 0, 0.9*Rc*math.cos(x*math.pi/3), 0.9*Rc*math.sin(x*math.pi/3) ))
	walledges.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Lo,0.9*Rc*math.cos(x*math.pi/3),0.9*Rc*math.sin(x*math.pi/3)))
	walledges.append(right)
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( Li-Transition, 0.9*Rc*math.cos(x*math.pi/3), 0.9*Rc*math.sin(x*math.pi/3) ))
	walledgesporo.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Transition,0.9*Rc*math.cos(x*math.pi/3),0.9*Rc*math.sin(x*math.pi/3)))
	walledgesporo.append(right)
for x in [0] :
	#inversed
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( 0, 0.9*Rc*math.cos(x*math.pi/3), 0.9*Rc*math.sin(x*math.pi/3) ))
	inversedwalledges.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Lo,0.9*Rc*math.cos(x*math.pi/3),0.9*Rc*math.sin(x*math.pi/3)))
	inversedwalledges.append(right)
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( Li-Transition, 0.9*Rc*math.cos(x*math.pi/3), 0.9*Rc*math.sin(x*math.pi/3) ))
	inversedwalledgesporo.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Transition,0.9*Rc*math.cos(x*math.pi/3),0.9*Rc*math.sin(x*math.pi/3)))
	inversedwalledgesporo.append(right)
for x in [0.25,0.75,1.25,1.75,2.25,2.75,3.25,3.75,4.25,4.75,5.25,5.75] :
	#innerandrings
	#rings
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( 0, Rc*math.cos(x*math.pi/3), Rc*math.sin(x*math.pi/3) ))
	innerandrings.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Lo,Rc*math.cos(x*math.pi/3),Rc*math.sin(x*math.pi/3)))
	innerandrings.append(right)
	left  = geompy.GetEdgeNearPoint(packedTube, geompy.MakeVertex( Li-Transition, Rc*math.cos(x*math.pi/3), Rc*math.sin(x*math.pi/3) ))
	innerandringsporo.append(left)
	right = geompy.GetEdgeNearPoint(packedTube,geompy.MakeVertex(Li+Lp+Transition,Rc*math.cos(x*math.pi/3),Rc*math.sin(x*math.pi/3)))
	innerandringsporo.append(right)
	#hexagonal
	left  = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( 0, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	innerandrings.append(left)
	right = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	innerandrings.append(right)
	poro = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li-Transition, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	innerandringsporo.append(poro)
	poro = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition, 0.6034*Rc*math.cos(x*math.pi/3), 0.6034*Rc*math.sin(x*math.pi/3) ))
	innerandringsporo.append(poro)
for x in [0,1,2,3,4,5] :
	#innerandrings
	#x rotor
	left  = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( 0, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	innerandrings.append(left)
	right = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Lo, 0.05*Rc*math.cos(x*math.pi/3), 0.05*Rc*math.sin(x*math.pi/3) ))
	innerandrings.append(right)
	poro = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li+Lp+Transition, 0.1*Rc*math.cos(x*math.pi/3), 0.1*Rc*math.sin(x*math.pi/3) ))
	innerandringsporo.append(poro)
	poro = geompy.GetEdgeNearPoint( packedTube, geompy.MakeVertex( Li-Transition, 0.1*Rc*math.cos(x*math.pi/3), 0.1*Rc*math.sin(x*math.pi/3) ))
	innerandringsporo.append(poro)

	

#Add groups to Study
#faces
all = geompy.SubShapeAll( packedTube, geompy.ShapeType["FACE"])
inlet = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "inlet" )
geompy.UnionList( inlet, inletFaces)
outlet = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "outlet" )
geompy.UnionList( outlet, outletFaces)
poroInlet = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "poroInlet" )
geompy.UnionList( poroInlet, poroInletFaces)
poroOutlet = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "poroOutlet" )
geompy.UnionList( poroOutlet, poroOutletFaces)
inletwall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "inletWall" )
geompy.UnionList( inletwall, inletWalls)
porowall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "poroWall" )
geompy.UnionList( porowall, poroWalls)
outletwall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "outletWall" )
geompy.UnionList( outletwall, outletWalls)
internals = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "internal" )
geompy.UnionList( internals, internal)
pinternals1 = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "pinternal1" )
geompy.UnionList( pinternals1, pinternal1)
pinternals2 = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "pinternal2" )
geompy.UnionList( pinternals2, pinternal2)
pinternals3 = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "pinternal3" )
geompy.UnionList( pinternals3, pinternal3)
Test = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "test" )
geompy.UnionList( Test, test)
wall = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "fixedWall" )
geompy.UnionList( wall, poroWalls + outletWalls + inletWalls)
sphereSurfaces = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "sphereSurfaces")
#Divided Disk doesnt work
#geompy.UnionList( sphereSurfaces, sphFaces )
#Rest = geompy.CreateGroup( packedTube, geompy.ShapeType["FACE"], "rest" )
geompy.UnionList( sphereSurfaces, all )
geompy.DifferenceList( sphereSurfaces, inletFaces + outletFaces + inletWalls + outletWalls + internal + poroInletFaces + poroOutletFaces + poroWalls + pinternal1 + pinternal2 + pinternal3 )

#volumes
inletzone = geompy.CreateGroup( packedTube, geompy.ShapeType["SOLID"], "inletzone" )
geompy.UnionList( inletzone, inletShapes)
outletzone = geompy.CreateGroup( packedTube, geompy.ShapeType["SOLID"], "outletzone" )
geompy.UnionList( outletzone, outletShapes)

#edges
xedgesinlet = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "xedgesinlet" )
geompy.UnionList( xedgesinlet, xinlet)
xedgesporo = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "xedgesporo" )
geompy.UnionList( xedgesporo, xporo)
xedgesoutlet = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "xedgesoutlet" )
geompy.UnionList( xedgesoutlet, xoutlet)
Walledges = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "walledges" )
geompy.UnionList( Walledges, walledges)
Walledgesporo = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "walledgesporo" )
geompy.UnionList( Walledgesporo, walledgesporo)
inversedWalledges = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "inversedwalledges" )
geompy.UnionList( inversedWalledges, inversedwalledges)
inversedWalledgesporo = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "inversedwalledgesporo" )
geompy.UnionList( inversedWalledgesporo, inversedwalledgesporo)
#all = geompy.SubShapeAll( packedTube, geompy.ShapeType["EDGE"])
#innerRings = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "innerAndRings" )
#geompy.UnionList( innerRings, all )
#geompy.DifferenceList( innerRings, xinlet + xporo + xoutlet + walledges + walledgesporo + inversedwalledges + inversedwalledgesporo)
innerAndRingsporo = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "innerAndRingsporo" )
geompy.UnionList( innerAndRingsporo, innerandringsporo)
innerAndRings = geompy.CreateGroup( packedTube, geompy.ShapeType["EDGE"], "innerAndRings" )
geompy.UnionList( innerAndRings, innerandrings)

###
### SMESH component
###

#import  SMESH, SALOMEDS
#from salome.smesh import smeshBuilder

#smesh = smeshBuilder.New(theStudy)
#Mesh_1 = smesh.Mesh(packedTube)
#NETGEN_2D3D = Mesh_1.Tetrahedron(algo=smeshBuilder.NETGEN_1D2D3D)
#isDone = Mesh_1.Compute()


## Set names of Mesh objects
#smesh.SetName(NETGEN_2D3D.GetAlgorithm(), 'NETGEN_2D3D')
#smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
