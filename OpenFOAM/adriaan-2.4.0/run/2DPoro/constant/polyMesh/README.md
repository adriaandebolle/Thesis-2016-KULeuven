Files (faces) are too big. </br>

Make mesh: </br>
Run "ideasUNVToFoam to get Mesh" </br>
Command $transformPoints "(0.001 0.001 0.001)" </br>
Use checkMesh and/or setSet to make some manipulations if necessary.</br>
Use createPatch to merge patches together or add undefined faces to a patch if necessary. </br>

For simulations results look to run (log) file and use file for gnuplot.
