import pytest
from inputparam import*
from data import*
import numpy as np

global d, d2, d3

d = SPData()
d2 = SPData()
d3 = SPData()

# --------------------------------------------
d = input_param("Input/Input_t1.txt", d)

def test_polarization():
    expected = [0., 1., 0.]
    assert np.allclose(d.pol , expected)


def test_direction():
    expected = [1, 0, 0]
    assert np.allclose(d.dir, expected)


def test_wavelength():
    expected_min = 400
    expected_max = 500
    assert ([d.wl_init, d.wl_final] == [expected_min, expected_max])


def test_steps():
    assert (d.num == 1)


def test_eps0():
    assert (d.eps0 == 0.00000000000885)


def test_mu0():
    assert d.mu0 == 0.00000125


def test_mu1():
    assert d.mu1 == 0.00000125


def test_gamma():
    assert d.gamma == 17.94


def test_plasmafreq():
    assert d.plasmafreq == 2165

def test_beta1():
    assert d.beta == 11600000000
# --------------------------------------------
d2 = input_param("Input/Input_t2.txt", d2)


def test_polarization2():
    expected = [1., 0., 0.]
    assert np.allclose(d2.pol , expected)


def test_direction2():
    expected = [0, 1, 0]
    assert np.allclose(d2.dir, expected)


def test_wavelength2():
    expected_min = 300
    expected_max = 400
    assert ([d2.wl_init, d2.wl_final] == [expected_min, expected_max])


def test_steps2():
    assert (d2.num == 5)


def test_eps02():
    assert (d2.eps0 == 0.000000885)


def test_mu02():
    assert d2.mu0 == 0.0000234


def test_mu12():
    assert d2.mu1 == 1


def test_gamma2():
    assert d2.gamma == 1


def test_plasmafreq2():
    assert d2.plasmafreq == 1

def test_beta2():
    assert d2.beta == 1
#--------------------------------------------------------
d3 = input_param("Input/Input_t3.txt", d3)


def test_polarization3():
    expected = [0., 0., 1.]
    assert np.allclose(d3.pol , expected)


def test_direction3():
    expected = [1,0,0]
    assert np.allclose(d3.dir, expected)


def test_wavelength3():
    expected_min = 500
    expected_max = 600
    assert ([d3.wl_init, d3.wl_final] == [expected_min, expected_max])


def test_steps3():
    assert (d3.num == 8)


def test_eps03():
    assert  (d3.eps0 == 1)


def test_mu03():
    assert d3.mu0 == 1


def test_mu13():
    assert d3.mu1 == 1


def test_gamma3():
    assert d3.gamma == 1


def test_plasmafreq3():
    assert d3.plasmafreq == 1

def test_beta3():
    assert d3.beta == 11