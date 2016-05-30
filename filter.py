###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Script to induce gaps and overlaps so slightly touching spheres are not possible
###
### Run with command: $python filter.py
###

import math, numpy

#parameters
Rc=51.4/2
Rsreal=1.5
scaleFactor = 1
Rs=scaleFactor*Rsreal
#Transition from structured mesh to position of sphere (not too abrupt)
Transition = 25
gap = 0.05*Rs
tolerance = 1e-7

#Loading centres
data = numpy.loadtxt('myYade/centresRandom3mm5550')

spheres = []

volume_spheres = 0
volume_spheres_wanted = 0
makeOnlyOverlap = 0
#Add loop to add all spheres
for index in range (0, len(data)) :
	#if data[index][2] < 0.00105*Rs and data[index][2] > -0.00105*Rs :	
			x = 1000*data[index][0]
			y = 1000*data[index][1]
			z = 1000*data[index][2]
			centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
			#Filter/Scale intersecting spheres
			radius = Rs
	 		#Sphere too close at border or not?
			centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
			iterationRoom = spheres
			if centreToCentre > Rc-gap-radius and centreToCentre < Rc-radius+gap :
				increase = Rc-radius+gap-centreToCentre
				radius = radius + increase
			for sphereCompare in spheres :
				[x2,y2,z2] = [sphereCompare[0],sphereCompare[1],sphereCompare[2]]
				dist = math.sqrt((x-x2)**2+(y-y2)**2+(z-z2)**2)
				volume_sphereCompare = 1.33333333333333333*math.pi*sphereCompare[3]**3
				radius_sphereCompare = sphereCompare[3]
				#Sphere overlapping not enough or too close?
				if dist < Rs+gap+radius_sphereCompare and dist > Rs-gap+radius_sphereCompare :
					#scale sphere
					#gap when porosity too low; overlap when porosity too high
					if volume_spheres < volume_spheres_wanted :
						#make overlapping
						print('overlap')
						newradius = dist+gap-radius_sphereCompare
						if radius < newradius :
							radius = newradius
					else : 
						#make gap
						print('gap')
						newradius = dist-gap-radius_sphereCompare
						if radius > newradius :
							radius = newradius 
			makeOnlyOverlaps = 0			
			spheres.append( [x,y,z,radius] )
			volume_spheres = volume_spheres + 1.33333333333333333*math.pi*radius**3
			volume_spheres_wanted = len(spheres)*1.333333333333333333*math.pi*Rs**3
			#sphere.UnRegister()
			print('step ' + str(index))

numpy.savetxt('spheres5550', spheres)

