from inputparam import input_param
from inputmesh import mesh_input
from data import SPData
from fem_solver import*
import time
from fem_output import*


for jj in [1,2,3]:

    data_obj = [SPData(), SPData()]

    paramfile = []
    geo_file = []
    geo_pr_file = []
    geo_fc_file = []

    paramfile.append("Input/Input_t1.txt")
    paramfile.append("Input/Input_t1.txt")

    geo_file.append("Mesh/G_shell_t"+str(jj)+".xml")
    geo_file.append("Mesh/G_fill_t"+str(jj)+".xml")

    geo_pr_file.append("Mesh/G_shell_pr_t"+str(jj)+".xml")
    geo_pr_file.append("Mesh/G_fill_pr_t"+str(jj)+".xml")

    geo_fc_file.append("Mesh/G_shell_fc_t"+str(jj)+".xml")
    geo_fc_file.append("Mesh/G_fill_fc_t"+str(jj)+".xml")

    for i in range(len(paramfile)):

        start_time = time.time()

        data_obj[i] = input_param(paramfile[i], data_obj[i])
        data_obj[i] = mesh_input(geo_file[i], geo_pr_file[i], geo_fc_file[i], data_obj[i])
        data_obj[i] = freq_fem_solver(data_obj[i])
        data_obj[i].label = "testid3" + "mesh_t" + str(jj) + "type" + str(i)
        fem_output(data_obj[i])

        print("----<< SPDFM Calculated Serie " + str(jj) + " Test" + str(i + 1) + " >>----")
        print("--- %s seconds ---" % (time.time() - start_time))




