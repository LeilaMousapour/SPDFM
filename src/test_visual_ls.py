
import pytest
import fenics as fn
from data import SPData
from fem_solver import plane_wave_source
from inputmesh import mesh_input
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import c, pi
import time



def expected_real_response(omega, space_1d):
    storage = np.zeros(len(space_1d))
    k = (2 * pi * omega / c) * 1e-9
    for i in range(len(space_1d)):
        storage[i] = np.cos(k * space_1d[i])
    return storage


def expected_imaginary_response(omega, space_1d):
    storage = np.zeros(len(space_1d))
    k = (2 * pi * omega / c) * 1e-9
    for i in range(len(space_1d)):
        storage[i] = - np.sin(k * space_1d[i])
    return storage


def test_ls(testnum, inputfile, input_mesh_g, input_mesh_pr, input_mesh_fc):

    start_time = time.time()
    # Define the mesh and data object:
    data_obj = SPData()
    data_obj = mesh_input(input_mesh_g, input_mesh_pr, input_mesh_fc, data_obj)
    mesh = fn.Mesh(data_obj.mesh)

    # Input the testcase input data:
    with open(inputfile) as txt_file:
        txt_reader = txt_file.read()
        txt_rows = txt_reader.splitlines()
        line_count = 0
        for row in txt_rows:
            row = row.split(',')
            if line_count == 0:
                data_obj.pol = np.array([float(row[0]), float(row[1]), float(row[2])])
                line_count += 1
            elif line_count == 1:
                data_obj.dir = np.array([float(row[0]), float(row[1]), float(row[2])])
                line_count += 1
            elif line_count == 2:
                data_obj.omega = float(row[0]) * 1e12

    # Define function space:
    fspace = fn.FunctionSpace(mesh, 'N1curl', 2)
    light_re, light_im = plane_wave_source(data_obj.pol, data_obj.dir, data_obj.omega, mesh)
    space_re = fn.interpolate(light_re, fspace)
    space_im = fn.interpolate(light_im, fspace)

    filename_real = "Test Output/testid2-" + str(testnum) + "_Efield_real.pvd"
    filename_im = "Test Output/testid2-" + str(testnum) + "_Efield_imag.pvd"

    file_real = fn.File(filename_real)
    file_im = fn.File(filename_im)

    file_real << space_re
    file_im << space_im

    return


# Test1:
test_ls(1, "Input/LS_t1.txt", "Mesh/G_cube_10node.xml",
        "Mesh/G_cube_10node_physical_region.xml", "Mesh/G_cube_10node_facet_region.xml")
print("Test1 done!")

# Test2:
test_ls(2, "Input/LS_t2.txt", "Mesh/G_cube_10node.xml",
        "Mesh/G_cube_10node_physical_region.xml", "Mesh/G_cube_10node_facet_region.xml")
print("Test2 done!")

# Test3:
test_ls(3, "Input/LS_t1.txt", "Mesh/G_cube_20node.xml",
        "Mesh/G_cube_20node_physical_region.xml", "Mesh/G_cube_20node_facet_region.xml")
print("Test3 done!")

# Test4:
test_ls(4, "Input/LS_t2.txt", "Mesh/G_cube_20node.xml",
        "Mesh/G_cube_20node_physical_region.xml", "Mesh/G_cube_20node_facet_region.xml")
print("Test4 done!")

# Test5:
test_ls(5, "Input/LS_t1.txt", "Mesh/G_cube_40node.xml",
        "Mesh/G_cube_40node_physical_region.xml", "Mesh/G_cube_40node_facet_region.xml")
print("Test5 done!")

# Test6:
test_ls(6, "Input/LS_t2.txt", "G_cube_40node.xml",
        "G_cube_40node_physical_region.xml", "G_cube_40node_facet_region.xml")
print("Test6 done!")
