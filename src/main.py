#    SPDFM Control Module   *
#
# Press the green button in the gutter to run the script.
import fenics as fn
import numpy as np
import sys
from inputparam import input_param
from inputmesh import mesh_input
from data import SPData
from fem_solver import*
from fem_output import fem_output
import time


def main():

    paramfile = input("Please input the path to "
                      "the light source info file:")

    geo_file = input("Please input the path to the meshed geometry xml file (geo.xml):")

    geo_pr_file = input("Please input the path to the file containing"
                        " physical regions of the meshed geometry "
                        "(geo_physical_region.xml):")

    geo_fc_file = input("Please input the path to the file containing "
                        "facet regions of the meshed gomerty ("
                        "geo_facet_region.xml):")

    data_obj = SPData()

    start_time = time.time()

    data_obj = input_param(paramfile, data_obj)

    data_obj = mesh_input(geo_file, geo_pr_file, geo_fc_file, data_obj)

    data_obj = freq_fem_solver(data_obj)

    fem_output (data_obj)

    print("SPDFM is done!")

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()

