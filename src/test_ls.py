
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

    # Define the direction to read the data:
    x = np.linspace(0, 40, 500)
    y = np.zeros(len(x))
    z = np.zeros(len(x))
    coords = np.dstack((x, y, z))[0]

    # Map real SPDFM result in the desired direction:
    dir_line_real = np.array(list(map(space_re, coords)))

    uline_real = np.zeros(len(dir_line_real))
    for i in range(len(dir_line_real)):
        uline_real[i] = dir_line_real[i][1]

    # Map imaginary SPDFM result in the desired direction:
    dir_line_imaginary = np.array(list(map(space_im, coords)))

    uline_imaginary = np.zeros(len(dir_line_imaginary))
    for i in range(len(dir_line_imaginary)):
        uline_imaginary[i] = dir_line_imaginary[i][1]

    # Calculate the expected answer:
    ana_real = expected_real_response(data_obj.omega, x)
    ana_imaginary = expected_imaginary_response(data_obj.omega, x)


    fig, ax = plt.subplots(2, 2, figsize=(15, 15))

    ax[0][0].plot(x, uline_real, label="SPDFM real part, Test " + str(testnum))
    ax[0][0].plot(x, ana_real, '--', label="Expected real part, Test " + str(testnum))
    ax[0][0].set_xlabel("Radial Position")
    ax[0][0].set_ylabel("Electric Field Density")
    ax[0][0].grid()
    ax[0][0].legend()

    ax[0][1].plot(x, (uline_real - ana_real), label="Test " + str(testnum))
    ax[0][1].set_xlabel("Radial Position")
    ax[0][1].set_ylabel("Difference from Expected Value")
    ax[0][1].grid()
    ax[0][1].legend()

    ax[1][0].plot(x, uline_imaginary, label="SPDFM imaginary part, Test " + str(testnum))
    ax[1][0].plot(x, ana_imaginary, '--', label="Expected imaginary part, Test " + str(testnum))
    ax[1][0].set_xlabel("Radial Position")
    ax[1][0].set_ylabel("Electric Field Density")
    ax[1][0].grid()
    ax[1][0].legend()

    ax[1][1].plot(x, (uline_imaginary - ana_imaginary), label="Test " + str(testnum))
    ax[1][1].set_xlabel("Radial Position")
    ax[1][1].set_ylabel("Difference from Expected Value")
    ax[1][1].grid()
    ax[1][1].legend()
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()

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
test_ls(6, "Input/LS_t2.txt", "Mesh/G_cube_40node.xml",
        "Mesh/G_cube_40node_physical_region.xml", "Mesh/G_cube_40node_facet_region.xml")
print("Test6 done!")
