import fenics as fn
from scipy.constants import pi, c
import numpy as np


def real_epsilon(omega, plasma, gamma):
    return (omega**2 - plasma**2 + gamma**2) / (omega**2 + gamma**2)


def imaginary_epsilon(omega, plasma, gamma):
    return (gamma * (plasma**2)) / (omega * (omega**2 + gamma**2))


class Permeability(fn.UserExpression):

    def __init__(self, mu0, mu1, markers, **kwargs):
        super().__init__(**kwargs)
        self.markers = markers
        self.mu0 = mu0
        self.mu1 = mu1

    def eval_cell(self, values, x, cell):
        if self.markers[cell.index] > 2:
            values[0] = self.mu0
        else:
            values[0] = self.mu1

    def value_shape(self):
        return (1,)


class RealPermittivity(fn.UserExpression):

    def __init__(self, omega, plasma, gamma, markers, **kwargs):
        super().__init__(**kwargs)
        self.markers = markers
        self.omega = omega
        self.plasma = plasma
        self.gamma = gamma

    def eval_cell(self, values, x, cell):

        if self.markers[cell.index] > 2:
            values[0] = 1
        else:
            values[0] = real_epsilon(self.omega, self.plasma, self.gamma)

    def value_shape(self):
        return (1,)


class ImagPermittivity(fn.UserExpression):

    def __init__(self, omega, plasma, gamma, markers, **kwargs):
        super().__init__(**kwargs)
        self.markers = markers
        self.markers = markers
        self.omega = omega
        self.plasma = plasma
        self.gamma = gamma

    def eval_cell(self, values, x, cell):
        if self.markers[cell.index] > 2:
            values[0] = 0
        else:
            values[0] = imaginary_epsilon(self.gamma, self.plasma, self.gamma)

    def value_shape(self):
        return (1,)


def plane_wave_source(p, d, omega, mesh):

    # Wavenumber (1/m)
    k = 2 * pi * omega / c

    # Convert wavenumber to 1/nm
    k = k * 1e-9

    # Real and imaginary part of light electric field:
    e_light_re = fn.Expression(("px*cos(k*(dx*x[0]+dy*x[1]+dz*x[2]))",
                                "py*cos(k*(dx*x[0]+dy*x[1]+dz*x[2]))",
                                "pz*cos(k*(dx*x[0]+dy*x[1]+dz*x[2]))"),
                               dx=d[0], dy=d[1], dz=d[2],
                               px=p[0], py=p[1], pz=p[2],
                               k=k, degree=2)

    e_light_im = fn.Expression(("-px*sin(k*(dx*x[0]+dy*x[1]+dz*x[2]))",
                                "-py*sin(k*(dx*x[0]+dy*x[1]+dz*x[2]))",
                                "-pz*sin(k*(dx*x[0]+dy*x[1]+dz*x[2]))"),
                               dx=d[0], dy=d[1], dz=d[2],
                               px=p[0], py=p[1], pz=p[2],
                               k=k, degree=2)

    return e_light_re, e_light_im


def freq_fem_solver(data_obj):

    # Mesh elements:
    mesh = data_obj.mesh
    markers = data_obj.markers
    boundaries = data_obj.boundaries

    # Defining differential elements:
    dx = fn.Measure('dx', domain=mesh, subdomain_data=markers)
#    ds = fn.Measure('ds', domain=mesh, subdomain_data=boundaries)

    # Sorting material properties:
    p = data_obj.pol
    d = data_obj.dir
    eps0 = float(data_obj.eps0)      # F/m
    #mu = Permeability(data_obj.mu0, data_obj.mu1, markers, degree=1)  # H/m
    mu = float(data_obj.mu0)
    plasma = float(data_obj.plasmafreq)
    gamma = float(data_obj.gamma)
    beta = float(data_obj.beta)

    # Sorting frequency range:
    omega1 = c / (data_obj.wl_init * 1e-9)  # 1/s
    omega2 = c / (data_obj.wl_final * 1e-9)  # 1/s
    num = int(data_obj.num)
    omegalist = np.linspace(omega1, omega2, num)

    for omega in omegalist:

        # Defining permittivity:
        #eps_r = RealPermittivity(omega, plasma, gamma, markers, degree=1)
        #eps_i = ImagPermittivity(omega, plasma, gamma, markers, degree=1)
        eps_r=real_epsilon(omega, plasma, gamma)
        eps_i=imaginary_epsilon(omega, plasma, gamma)

        # Defining space element:
        efield_element = fn.FiniteElement('N1curl', fn.tetrahedron, 2)
        jfield_element = fn.FiniteElement('RT', fn.tetrahedron, 2)
        mixed_element = fn.MixedElement([efield_element, efield_element,
                                         jfield_element, jfield_element])

        # Define complex function spaces:
        func_space = fn.FunctionSpace(mesh, mixed_element)
        (te_r, te_i, tj_r, tj_i) = fn.TestFunctions(func_space)
        (e_r, e_i, j_r, j_i) = fn.TrialFunctions(func_space)

        # Setting up the light source := inner boundary conditions:
        inner_bc_re, inner_bc_im = plane_wave_source(p, d, omega, mesh)

        # Setting up the boundary condition in the infinity:
        outer_bc_re = fn.Constant(("0", "0", "0"))
        outer_bc_im = fn.Constant(("0", "0", "0"))

        # Applying boundary conditions to the function spaces:
        outer_boundary_e_re = fn.DirichletBC(func_space.sub(0),
                                             outer_bc_re, boundaries, 2)
        outer_boundary_e_im = fn.DirichletBC(func_space.sub(1),
                                             outer_bc_im, boundaries, 2)
        outer_boundary_j_re = fn.DirichletBC(func_space.sub(2),
                                             outer_bc_re, boundaries, 2)
        outer_boundary_j_im = fn.DirichletBC(func_space.sub(3),
                                             outer_bc_im, boundaries, 2)

        inner_boundary_e_re = fn.DirichletBC(func_space.sub(0),
                                             inner_bc_re,
                                             boundaries, 1)
        inner_boundary_e_im = fn.DirichletBC(func_space.sub(1),
                                             inner_bc_im,
                                             boundaries, 1)
        inner_boundary_j_re = fn.DirichletBC(func_space.sub(2),
                                             fn.Constant(("0", "0", "0")),
                                             boundaries, 2)
        inner_boundary_j_im = fn.DirichletBC(func_space.sub(3),
                                             fn.Constant(("0", "0", "0")),
                                             boundaries, 2)

        boundary_condition = [inner_boundary_e_re, inner_boundary_e_im,
                              outer_boundary_e_re, outer_boundary_e_im,
                              inner_boundary_j_re, inner_boundary_j_im,
                              outer_boundary_j_re, outer_boundary_j_im]

        # Defining zero elements:
        zero_function = fn.Constant(("0", "0", "0"))
        source_function = fn.Constant(("0", "0", "0"))

        # Defining equation matrix:
        # First row:
        aa = (1 / float(mu)) * fn.inner(fn.curl(te_r), fn.curl(e_r))\
            * dx - omega * omega * float(eps_i) * fn.inner(te_i, e_r)\
            * dx - omega * omega * float(eps_r) * fn.inner(te_r, e_r) * dx

        ab = (-1 / float(mu)) * fn.inner(fn.curl(te_r), fn.curl(e_i)) * dx\
            + omega * omega * float(eps_i) * fn.inner(te_r, e_i) * dx\
            + omega * omega * float(eps_r) * fn.inner(te_r, e_i) * dx

        ac = omega * fn.inner(tj_i, j_r) * dx

        ad = omega * fn.inner(tj_r, j_i) * dx

        # Second row:
        ba = (1 / float(mu)) * fn.inner(fn.curl(te_i), fn.curl(e_r)) * dx \
            + omega * omega * float(eps_i) * fn.inner(te_r, e_r) * dx \
            - omega * omega * float(eps_r) * fn.inner(te_i, e_r) * dx

        bb = (1 / float(mu)) * fn.inner(fn.curl(te_r), fn.curl(e_i)) * dx \
            + omega * omega * float(eps_i) * fn.inner(te_i, e_i) * dx \
            - omega * omega * float(eps_r) * fn.inner(te_r, e_i) * dx

        bc = -omega * fn.inner(tj_r, j_r) * dx

        bd = omega * fn.inner(tj_i, j_i) * dx

        # Third row:
        ca = omega * plasma * plasma * eps0 * fn.inner(te_i, e_r) * dx

        cb = omega * plasma * plasma * eps0 * fn.inner(te_r, e_i) * dx

        cc = -1 * beta * fn.div(tj_r) * fn.div(j_r) * dx \
            + omega * omega * fn.inner(tj_r, j_r) * dx \
            - omega * gamma * fn.inner(tj_i, j_r) * dx

        cd = beta * fn.div(tj_i) * fn.div(j_i) * dx \
            - omega * omega * fn.inner(tj_i, j_i) * dx \
            - omega * gamma * fn.inner(tj_r, j_i) * dx

        # Fourth row:
        da = -1 * omega * plasma * plasma * eps0 * fn.inner(te_r, e_r) * dx

        db = omega * plasma * plasma * eps0 * fn.inner(te_i, e_i) * dx

        dc = -1 * beta  * fn.div(tj_i) * fn.div(j_r) * dx \
            + omega * omega * fn.inner(tj_i, j_r) * dx \
            + omega * gamma * fn.inner(tj_r, j_r) * dx

        dd = -1 * beta * beta * fn.div(tj_r) * fn.div(j_i) * dx \
            + omega * omega * fn.inner(tj_r, j_i) * dx \
            - omega * gamma * fn.inner(tj_i, j_i) * dx

        # Left Matrix:
        L = aa + ab + ac + ad +\
            ba + bb + bc + bd +\
            ca + cb + cc + cd +\
            da + db + dc + dd

        # Right Matrix:
        R = fn.inner(zero_function, te_r) * dx +\
            fn.inner(zero_function, te_i) * dx +\
            fn.inner(source_function, tj_r) * dx +\
            fn.inner(source_function, tj_i) * dx

        solution = fn.Function(func_space)

        fn.solve(L == R, solution, bcs=boundary_condition,
                 solver_parameters={'linear_solver': 'mumps'})

        e_re_calc, e_im_calc, j_re_calc, j_im_calc = solution.split()

        data_obj.e_real.append(e_re_calc)
        data_obj.e_im.append(e_im_calc)
        data_obj.j_real.append(j_re_calc)
        data_obj.j_im.append(j_im_calc)

    return data_obj