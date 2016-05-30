###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Generate compact BCC packing, randomize by shaking
### and compression to defined volume to get desired porosity 
###
### Script to load into Yade (DEM tool)
###

import numpy
import math

#parameters
Rc=0.0514/2
Rsreal=0.0015
Rs=1.02*Rsreal
Li=0.2
Lp=0.304/5
Lo=0.2
volumep = Lp*math.pi*Rc**2
volumes = 1.3333333333*math.pi*Rsreal**3
eps = 0.355
amount = 5550 #int(((1-eps)*volumep)/volumes)

# import yade modules that we will use below
from yade import utils, export

# create cylindre and two movable faces to compress
body = O.bodies.append(geom.facetCylinder(center=(0,0,0.75*Lp),radius=Rc,height=1.5*Lp,segmentsNumber=150))
top = O.bodies.append(geom.facetCylinder(center=(0,0,1.5*Lp),radius=Rc,height=0,segmentsNumber=150))
bottom = O.bodies.append(geom.facetCylinder(center=(0,0,0),radius=Rc,height=0,segmentsNumber=150))

#create dense regular packing 
lengthSteps = 2*int(Lp//(4*Rs/math.sqrt(3)))
ySteps = 2*int((2*Rc)//(4*Rs/math.sqrt(3)))
zSteps = ySteps
added = 0
for i in range (0,lengthSteps) :
    for k in range (-ySteps,ySteps) :
	for l in range (-zSteps,zSteps) :
		x = 0.1*Lp+(2+i*4)*Rs/math.sqrt(3)
		y = (2+k*4)*Rs/math.sqrt(3)
		z = (2+l*4)*Rs/math.sqrt(3)
		centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
		if centreToCentre < Rc-Rs and added < amount:
      			O.bodies.append(utils.sphere((z,y,x),Rs))
			added=added+1
		x = 0.1*Lp+i*4*Rs/math.sqrt(3)
		y = k*4*Rs/math.sqrt(3)
		z = l*4*Rs/math.sqrt(3)
		centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
		if centreToCentre < Rc-Rs and added < amount:
      			O.bodies.append(utils.sphere((z,y,x),Rs))
			added=added+1


#apply motion and compression
O.engines=[
   ForceResetter(),
   InsertionSortCollider([Bo1_Sphere_Aabb(),Bo1_Facet_Aabb()]),
   InteractionLoop(
      # handle sphere+sphere and facet+sphere collisions
      [Ig2_Sphere_Sphere_L3Geom(),Ig2_Facet_Sphere_L3Geom()],
      [Ip2_FrictMat_FrictMat_FrictPhys()],
      [Law2_L3Geom_FrictPhys_ElPerfPl()]
   ),
   NewtonIntegrator(gravity=(0,0,-9.81),damping=0.9),
   HarmonicMotionEngine(A=(0.05*Lp,0.05*Lp,0.05*Lp),f=(100,100,100),ids=body, label='shaker'),
   TranslationEngine(translationAxis=(0,0,1),velocity=2.5*Lp,ids=bottom,dead=True, label='bottomComp'),
   TranslationEngine(translationAxis=(0,0,-1),velocity=2.5*Lp,ids=top,dead=True, label='topComp'),
   PyRunner(command='changeShake1()',virtPeriod=0.02),
   PyRunner(command='changeShake2()',virtPeriod=0.14),
   PyRunner(command='changeShake3()',virtPeriod=0.04),
   PyRunner(command='changeShake3()',virtPeriod=0.16),
   PyRunner(command='startCompression()',virtPeriod=0.04),
   PyRunner(command='stopCompression()',virtPeriod=0.04+0.099),
   PyRunner(command='write()',virtPeriod=0.15),
]
O.dt=.5*PWaveTimeStep()

def changeShake1():
   shaker.A = (0.05*Lp,0.05*Lp,-0.05*Lp)
def changeShake2():
   shaker.A = (0,0,0.05*Lp)
   shaker.f=(0,0,100)
   shaker.fixed = False
def changeShake3():
   shaker.A=(0,0,0)
   shaker.f=(0,0,0)
   shaker.fixed = True
def startCompression():
   topComp.dead = False
   bottomComp.dead = False
def stopCompression():
   topComp.dead = True
   bottomComp.dead = True
   topComp.velocity = 0
   topComp.fixed = True
   bottomComp.velocity = 0
   bottomComp.fixed = True
def write():
   export.text('randomPacking'+str(int(2000*Rsreal))+'mm'+str(amount))
   O.pause()
