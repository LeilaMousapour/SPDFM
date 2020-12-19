#
# Input Paramaters Module
# ---------------------
# Module to input the light source
# properties and material properties:
# ---------------------
# Paramfile:
# line1: p1, p2, p3 (polarization)
# line2: d1, d2, d3 (directioin of the incidence)
# line3: w1 (initial wavelength of the source)
# line4: w2 (final wavelength of the source)
# line5: n (number of wavelengths in the given interval)
# line6: epsilon_0 (vacuum permittivity)
# line7: mu_0 (vacuum permeability)
# line8: mu_1 (medium permeability)
# line9: gamma (plasmon damping parameter of the geometry)
# line10: frequency (plasmon frequency of the medium)
#
# -----------------------------------------------------------------

import numpy as np
from spdfm_const import ConstParam


def input_param(paramfile, data_obj):

    cst = ConstParam()

    with open(paramfile) as txt_file:
        txt_reader = txt_file.read()
        txt_rows = txt_reader.splitlines()
        line_count = 0
        for row in txt_rows:
            row = row.split(',')
            if line_count == 0:
                data_obj.pol = np.array([float(row[0]),
                                         float(row[1]), float(row[2])])
                if np.inner(data_obj.pol, data_obj.pol) > cst.pol_lmt:
                    raise ValueError("Polarization Vector"
                                     " Amplitude out of Range")
                line_count += 1

            elif line_count == 1:
                data_obj.dir = [float(row[0]), float(row[1]), float(row[2])]
                if abs(np.inner(data_obj.dir,
                                data_obj.dir) - 1.0) > cst.tol_gen:
                    raise ValueError("Direction Vector not Normallized")
                if abs(np.inner(data_obj.pol, data_obj.dir)) > cst.tol_gen:
                    raise ValueError("Not Orthogonal Light Source")
                line_count += 1

            elif line_count == 2:
                data_obj.wl_init = float(row[0])
                if data_obj.wl_init > cst.wl_max_lmt\
                        or data_obj.wl_init < cst.wl_min_lmt:
                    raise ValueError("Wavelength out of Range")
                line_count += 1

            elif line_count == 3:
                data_obj.wl_final = float(row[0])
                if data_obj.wl_final > cst.wl_max_lmt\
                        or data_obj.wl_final < cst.wl_min_lmt:
                    raise ValueError("Wavelength out of Range")
                line_count += 1

            elif line_count == 4:
                data_obj.num = float(row[0])
                line_count += 1

            elif line_count == 5:
                data_obj.eps0 = float(row[0])
                line_count += 1

            elif line_count == 6:
                data_obj.mu0 = float(row[0])
                line_count += 1

            elif line_count == 7:
                data_obj.mu1 = float(row[0])
                line_count += 1

            elif line_count == 8:
                data_obj.gamma = float(row[0])
                line_count += 1

            elif line_count == 9:
                data_obj.plasmafreq = float(row[0])
                line_count += 1

            elif line_count == 10:
                data_obj.beta = float(row[0])
                line_count += 1

    line_count += 1

    print(f'Processed {line_count} lines (MP file).')
    return(data_obj)
