import fenics as fn


def fem_output(data_obj):

    length = len(data_obj.e_real)

    for i in range(length):
        e_re_calc = data_obj.e_real[i]
        e_im_calc = data_obj.e_im[i]
        j_re_calc = data_obj.j_real[i]
        j_im_calc = data_obj.j_im[i]

        file_e_re = fn.File("FEM Output/E_real_wavelength" +
                            str(i) + "_" + data_obj.label + ".pvd")
        file_e_im = fn.File("FEM Output/E_im_wavelength" +
                            str(i) + "_" + data_obj.label + ".pvd")
        file_j_re = fn.File("FEM Output/J_re_wavelength" +
                            str(i) + "_" + data_obj.label + ".pvd")
        file_j_im = fn.File("FEM Output/J_im_wavelength" +
                            str(i) + "_" + data_obj.label + ".pvd")

        file_e_re << e_re_calc
        file_e_im << e_im_calc
        file_j_re << j_re_calc
        file_j_im << j_im_calc



