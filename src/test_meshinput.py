from inputparam import input_param
from inputmesh import mesh_input
from data import SPData
from fem_solver import*
import time
import matplotlib.pyplot as plt
from fem_output import*

for jj in [1,2,3]:

    data_obj = SPData

    paramfile = []
    geo_file = []
    geo_pr_file = []
    geo_fc_file = []

    geo_file = "Mesh/G_shell_t"+str(jj)+".xml"

    geo_pr_file = ("Mesh/G_shell_pr_t"+str(jj)+".xml")

    geo_fc_file = ("Mesh/G_shell_fc_t"+str(jj)+".xml")

    data_obj = mesh_input(geo_file, geo_pr_file, geo_fc_file, data_obj)

    mesh = fn.Mesh(data_obj.mesh)

    plt.figure(jj)
    fn.plot(mesh)
    plt.show()

