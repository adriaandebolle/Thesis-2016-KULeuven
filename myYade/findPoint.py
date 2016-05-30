###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Interactive terminal interface to find centroid close to a point
### Interesting to locate mesh problems and manipulate geometry.
###
### Script to open with python (command $python findPoint.py)
###

import numpy
import math
amount = raw_input("Please enter amount spheres in unit: ")
print ("you entered " + str(amount))
data = numpy.loadtxt('centresRandom3mm'+str(int(amount)))
xcoord = raw_input("Please enter x-coord (mm): ")
xcoord = float(xcoord)/1000
print ("you entered " + str(xcoord))
ycoord = raw_input("Please enter y-coord (mm): ")
ycoord = float(ycoord)/1000
print ("you entered " + str(ycoord))
zcoord = raw_input("Please enter z-coord (mm): ")
zcoord = float(zcoord)/1000
print ("you entered " + str(zcoord))
pointindex = 0
error = (xcoord-data[0][0])**2+(ycoord-data[0][1])**2+(zcoord-data[0][2])**2
smaller = 0
for index in range (1,len(data)) :
	errorindex = (xcoord-data[index][0])**2+(ycoord-data[index][1])**2+(zcoord-data[index][2])**2
	if data[index][0] < xcoord :
		smaller = smaller + 1
	if errorindex < error :
		error = errorindex
		pointindex = index
print('Closest point has index: '+str(pointindex))
print('It has coordinates (mm): x '+str(data[pointindex][0]*1000)+' y '+str(data[pointindex][1]*1000)+' z '+str(data[pointindex][2]*1000))
print('There are ' + str(smaller) + ' spheres smaller.')
