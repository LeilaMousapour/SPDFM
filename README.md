# SPDFM User Guid

The problem statement for this software can be found in: 
https://github.com/shmouses/SPDFM/blob/master/docs/ProblemStatement/ProblemStatement.pdf

The systerm requirement specification document that includes the theoretical background can be found in: 
https://github.com/shmouses/SPDFM/blob/master/docs/SRS/SRS.pdf

The validation and verification plan and report are respectively documented in:
https://github.com/shmouses/SPDFM/blob/master/docs/VnVPlan/VnVPlan.pdf
and 
https://github.com/shmouses/SPDFM/blob/master/docs/VnV%20Report/VnV%20Report.pdf

The modular desing of the software is docuented in: 
https://github.com/shmouses/SPDFM/blob/master/docs/Design

For the first time user's of SPDFM, using the tutorial jupyter notebook is highly recommended.
The link to Tutorial Jupyter notebook: 
https://github.com/shmouses/SPDFM/blob/master/src/SPDFM%20Tutorial%20.ipynb

For running SPDFM on a system below libraries should be install on the system:
-fenicd 2019 1.0
-matplolib
-numpy
-math
-time
-scipy

As SPDFM is written based on fenics toolbox, this program should be run on a system with Linux OS.

To initiate running a simulation on SPDFM: 

0-download or clone src folder on your system

1-Run the main.py

2-User will be asked to provide a path to the input file. This file contains information about material properties and light source illumination
  If src file is copied user can insert: Input/Input_t1.txt

3-User will be asked to provide the path to the .xml mesh file. Be aware that this mesh should be readable by dolfin toolbox which is a embeded toolbox being used in fenics.
  Sample input: Mesh/G_fill_t1.xml
  
4-User will be asked to provide the path to the file that indicates physical regions in the mesh.
  Sample input: Mesh/G_fill_pr_t1.xml
  
5-User will be ask to provide the path to the file that contains facet regions information for the mesh.
  Sample input: Mesh?G_fill_fc_t1.xml

6-It takes a while for SPDFM to run the calculations and save the real and imaginary parts of the electric field and electric current density in .pvd and .vtk files in "FEM Output"

** for testing different areas of the code user can simply run .py files that start with "test_". For executing test_constparam.py and test_inputparam.py user should use pytest library python for execution.

