# Data Structure Module
# -----------------------------

class SPData(object):
    def __init__(self):

        # Light source properties
        self.pol = None
        self.dir = None
        self.wl_init = None
        self.wl_final = None
        # --------------------------------------------------------------

        # Material properties
        self.num = None
        self.eps0 = None
        self.mu0 = None
        self.mu1 = None
        self.beta = None
        self.gamma = None
        self.plasmafreq = None
        # --------------------------------------------------------------

        # Mesh
        self.mesh = None
        self.markers = None
        self.boundaries = None
        # --------------------------------------------------------------

        # Results
        self.e_real = []
        self.e_im = []
        self.j_real = []
        self.j_im = []
        self.label = "test"

