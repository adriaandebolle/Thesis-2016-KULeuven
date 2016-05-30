###
### Author: Adriaan De Bolle, student KULeuven
### Promotor: Prof. Simon Kuhn; Supervisor: Milad Mottaghi
### Thesis: Simulation of Darcy and non-Darcy flow through well-structured porous media
### Script description: Adapt coordinates of Yade to load into Salome
###
### Script to open with python
###

import numpy
Rs = 0.0015
centres = []
#gap=0.01*Rs
data = numpy.loadtxt('randomPacking3mm5550')
zcoord = []
for index in range (0,len(data)) :
	z = data[index][2]
	zcoord.append(z)
minimum = min(zcoord)

for index in range (0,len(data)) :
	z = data[index][0]
	y = data[index][1]
	x = data[index][2]-minimum+(1)*Rs
	centres.append([x,y,z])
max = 0
for index in range (0,len(centres)) :
	if centres[index][0] > max : 
		max = centres[index][0]

print(str(max))
numpy.savetxt('centresRandom3mm5550', centres)
