###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Creating a random distribution of spheres and export coordinates of sphere centres
###
### Script to load into Salome
###

import math
import numpy 
import random

#parameters
Rc=0.0257
Rs=0.0005
Li=0.2
Lp=0.304
Lo=0.2

Transition = 0.015

centres = []
spheres = []

#Because of gap 1% there is 2% space lost = It keeps adapting positions
#With 0,1% it is only 0,2%
#Making random packing
#parameters
eps = 0.35
gap = -0.05*Rs
Vp = Lp*math.pi*Rc**2
Vs = 1.33333333333333333*math.pi*Rs**3
Lpi=4*Rs
steps=int(Lp/Lpi)
Vpi=Lpi*math.pi*Rc**2
amount = int((1-eps)*Vp/Vs)
amounti = int((1-eps)*Vpi/Vs)
#3963*(1-eps)

# radialstepgenerator
radialsteps = []
bla = []
bla.append(0)

k = 0
radialsteps.append(k)
#step at least 20 spheres
while k < 1 :
	if k < 0.5 :
		k = k + 0.05
	elif k < 1 :
		k = k + 0.025
	else :
		k = k + 0.05
	radialsteps.append(k)
#looping until amount of spheres is reached
for step in range (0,steps) :
	amountir = 0
	amountirlast = 0
	bla[0] = step
	numpy.savetxt('centresTemp.txt', bla)
	for iterator in range (1, len(radialsteps)) :
		i=0
		iterations = 0
		rcupper=radialsteps[iterator]*Rc
		rclower=Rc*(radialsteps[iterator-1])
		if radialsteps[iterator] != radialsteps[len(radialsteps)-1] :
			rcmoreupper=Rc*(radialsteps[iterator+1])
		else :
			rcmoreupper = 0
		Vpir=Lpi*math.pi*rcupper**2-Lpi*math.pi*rclower**2
		Vpirmoreupper=Lpi*math.pi*rcmoreupper**2-Lpi*math.pi*rcupper**2
		amountirlast = amountir
		amountir = int(amounti*Vpir/Vpi)
		amountirnext = int(amounti*Vpirmoreupper/Vpi)
		while i < amountir :
		#creating random coordinates 
	   		x = Li+random.uniform(step*Lpi,(step+1)*Lpi)
			r = random.uniform(radialsteps[iterator-1]*Rc,radialsteps[iterator]*Rc)
			theta = random.uniform(0,2*math.pi)
	   		y = r*math.cos(theta)
	   		z = r*math.sin(theta)
			if iterations < 2*amountir :
				centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
		   		if centreToCentre < Rc-Rs-gap :
		   			add = 1
		   			dist = 0
					startrange = len(centres)-i-amountirlast
					#check if new sphere overlaps with spheres in own cell or neighboring 
		   			for index in range(startrange,len(centres)) :
						dist = math.sqrt((x-centres[index][0])**2+(y-centres[index][1])**2+(z-centres[index][2])**2)
						if dist < 2*Rs+gap :
				   			#don't add
				   			add = 0 
							iterations=iterations+1
				   			break
					if step != 0 and rcmoreupper!=0:
						for index in range(len(centres)-i-amountirlast-amounti-2,len(centres)-i-amounti+amountir+amountirnext+2) :
							dist = math.sqrt((x-centres[index][0])**2+(y-centres[index][1])**2+(z-centres[index][2])**2)
							if dist < 2*Rs+gap :
					   			#don't add
					   			add = 0 
								iterations=iterations+1
					   			break
					elif step != 0 and rcmoreupper==0 :
						for index in range(len(centres)-i-amountirlast-amounti-2,len(centres)-i-amounti+amountir+2) :
							dist = math.sqrt((x-centres[index][0])**2+(y-centres[index][1])**2+(z-centres[index][2])**2)
							if dist < 2*Rs+gap :
					   			#don't add
					   			add = 0 
								iterations=iterations+1
					   			break
		  			if add == 1 :
		   				centres.append([x,y,z])
		   				i = i + 1
						numpy.savetxt('centresInDisksTemp.txt', centres)
			else :
			#too much iteration; changing coordinates of already added spheres
				change = int(i*0.1)
				iterations = 0
				changeposition = len(centres)-1-random.randint(0,i)
				for x in range (0,change) :
					x = Li+random.uniform(step*Lpi,(step+1)*Lpi)
					r = random.uniform(radialsteps[iterator-1]*Rc,radialsteps[iterator]*Rc)
					theta = random.uniform(0,2*math.pi)
		   			y = r*math.cos(theta)
		   			z = r*math.sin(theta)
					centreToCentre = math.sqrt(abs(y)**2+abs(z)**2)
			   		if centreToCentre < Rc-Rs-gap :
			   			add = 1
			   			dist = 0
						startrange = len(centres)-i-amountirlast
			   			for index in range(startrange,len(centres)) :
							dist = math.sqrt((x-centres[index][0])**2+(y-centres[index][1])**2+(z-centres[index][2])**2)
							if dist < 2*Rs+gap :
					   			#don't add
								add = 0
					   			break
						if step != 0 and rcmoreupper!=0:
							for index in range(len(centres)-i-amountirlast-amounti-2,len(centres)-i-amounti+amountir+amountirnext+2) :
								dist = math.sqrt((x-centres[index][0])**2+(y-centres[index][1])**2+(z-centres[index][2])**2)
								if dist < 2*Rs+gap :
						   			#don't add
						   			add = 0 
						   			break
						elif step !=0 and rcmoreupper==0 :
							for index in range(len(centres)-i-amountirlast-amounti-2,len(centres)-i-amounti+amountir+2) :
								dist = math.sqrt((x-centres[index][0])**2+(y-centres[index][1])**2+(z-centres[index][2])**2)
								if dist < 2*Rs+gap :
						   			#don't add
						   			add = 0 
						   			break
			  			if add == 1 :
			   				centres[changeposition]=[x,y,z]
				
			
				
#end of while loop
#Centres of random packing generated
numpy.savetxt('centresCompletelyRandom.txt', centres)
