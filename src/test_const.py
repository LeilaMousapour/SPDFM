import pytest
from data import SPData
from spdfm_const import ConstParam

data_const = ConstParam()

def test_constant_param():
    ConstParam()
    storedvalues = [data_const.tol_gen, data_const.tol_fenics,
                    data_const.pol_lmt, data_const.wl_min_lmt,
                    data_const.wl_max_lmt]
    expected = [1e-5, 1e-10, 100, 200, 700]
    assert storedvalues == expected
