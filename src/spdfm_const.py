# Constant parameter module


class ConstParam(object):
    def __init__(self):
        self.tol_gen = 1e-5
        self.tol_fenics = 1e-10
        self.pol_lmt = 100
        self.wl_min_lmt = 200
        self.wl_max_lmt = 700
