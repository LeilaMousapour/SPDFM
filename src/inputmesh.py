#
#     Mesh Input Module
#
#


import fenics as fn


def mesh_input(geo, geo_pr, geo_fc, data_obj):

    data_obj.mesh = fn.Mesh(geo)
    data_obj.markers = fn.MeshFunction("size_t", data_obj.mesh, geo_pr)
    data_obj.boundaries = fn.MeshFunction("size_t", data_obj.mesh, geo_fc)

    return(data_obj)
