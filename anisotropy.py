import meep as mp
import math
import numpy as np
import matplotlib.pyplot as plt

resolution = 30  # pixels/μm

dpml = 1.0  # PML thickness
dsub = 1.0  # substrate thickness
dpad = 1.0  # padding thickness

k_point = mp.Vector3(0, 0, 0)

pml_layers = [mp.PML(thickness=dpml, direction=mp.X)]

n_0 = 1.55
delta_n = 0.159
epsilon_diag = mp.Matrix(
    mp.Vector3(n_0**2, 0, 0),
    mp.Vector3(0, n_0**2, 0),
    mp.Vector3(0, 0, (n_0 + delta_n) ** 2),
)

wvl = 0.54  # center wavelength
fcen = 1 / wvl  # center frequency


def pol_grating(d, ph, gp, nmode):
    sx = dpml + dsub + d + d + dpad + dpml
    sy = gp

    cell_size = mp.Vector3(sx, sy, 0)

    # twist angle of nematic director; from equation 1b
    def phi(p):
        xx = p.x - (-0.5 * sx + dpml + dsub)
        if (xx >= 0) and (xx <= d):
            return math.pi * p.y / gp + ph * xx / d
        else:
            return math.pi * p.y / gp - ph * xx / d + 2 * ph

    # return the anisotropic permittivity tensor for a uniaxial, twisted nematic liquid crystal
    def lc_mat(p):
        # rotation matrix for rotation around x axis
        Rx = mp.Matrix(
            mp.Vector3(1, 0, 0),
            mp.Vector3(0, math.cos(phi(p)), math.sin(phi(p))),
            mp.Vector3(0, -math.sin(phi(p)), math.cos(phi(p))),
        )
        lc_epsilon = Rx * epsilon_diag * Rx.transpose()
        lc_epsilon_diag = mp.Vector3(lc_epsilon[0].x, lc_epsilon[1].y, lc_epsilon[2].z)
        lc_epsilon_offdiag = mp.Vector3(
            lc_epsilon[1].x, lc_epsilon[2].x, lc_epsilon[2].y
        )
        return mp.Medium(
            epsilon_diag=lc_epsilon_diag, epsilon_offdiag=lc_epsilon_offdiag
        )

    geometry = [
        mp.Block(
            center=mp.Vector3(-0.5 * sx + 0.5 * (dpml + dsub)),
            size=mp.Vector3(dpml + dsub, mp.inf, mp.inf),
            material=mp.Medium(index=n_0),
        ),
        mp.Block(
            center=mp.Vector3(-0.5 * sx + dpml + dsub + d),
            size=mp.Vector3(2 * d, mp.inf, mp.inf),
            material=lc_mat,
        ),
    ]

    # linear-polarized planewave pulse source
    src_pt = mp.Vector3(-0.5 * sx + dpml + 0.3 * dsub, 0, 0)
    sources = [
        mp.Source(
            mp.GaussianSource(fcen, fwidth=0.05 * fcen),
            component=mp.Ez,
            center=src_pt,
            size=mp.Vector3(0, sy, 0),
        ),
        mp.Source(
            mp.GaussianSource(fcen, fwidth=0.05 * fcen),
            component=mp.Ey,
            center=src_pt,
            size=mp.Vector3(0, sy, 0),
        ),
    ]

    sim = mp.Simulation(
        resolution=resolution,
        cell_size=cell_size,
        boundary_layers=pml_layers,
        k_point=k_point,
        sources=sources,
        default_material=mp.Medium(index=n_0),
    )

    tran_pt = mp.Vector3(0.5 * sx - dpml - 0.5 * dpad, 0, 0)
    tran_flux = sim.add_flux(
        fcen, 0, 1, mp.FluxRegion(center=tran_pt, size=mp.Vector3(0, sy, 0))
    )

    sim.run(until_after_sources=100)

    input_flux = mp.get_fluxes(tran_flux)

    sim.reset_meep()

    sim = mp.Simulation(
        resolution=resolution,
        cell_size=cell_size,
        boundary_layers=pml_layers,
        k_point=k_point,
        sources=sources,
        geometry=geometry,
    )

    tran_flux = sim.add_flux(
        fcen, 0, 1, mp.FluxRegion(center=tran_pt, size=mp.Vector3(0, sy, 0))
    )

    sim.run(until_after_sources=300)

    res1 = sim.get_eigenmode_coefficients(
        tran_flux, range(1, nmode + 1), eig_parity=mp.ODD_Z + mp.EVEN_Y
    )
    res2 = sim.get_eigenmode_coefficients(
        tran_flux, range(1, nmode + 1), eig_parity=mp.EVEN_Z + mp.ODD_Y
    )
    angles = [math.degrees(math.acos(kdom.x / fcen)) for kdom in res1.kdom]

    return input_flux[0], angles, res1.alpha[:, 0, 0], res2.alpha[:, 0, 0];
#The properties of the two gratings are computed over the thickness range of 0.1 to 3.4 μm corresponding to phase delays  of approximately 0 to 1.

ph_uniaxial = 0  # chiral layer twist angle for uniaxial grating
ph_twisted = 70  # chiral layer twist angle for bilayer grating
gp = 6.5  # grating period
nmode = 5  # number of mode coefficients to compute
dd = np.arange(0.2, 3.5, 0.2)  # chiral layer thickness

m0_uniaxial = np.zeros(dd.size)
m1_uniaxial = np.zeros(dd.size)
ang_uniaxial = np.zeros(dd.size)

m0_twisted = np.zeros(dd.size)
m1_twisted = np.zeros(dd.size)
ang_twisted = np.zeros(dd.size)

for k in range(len(dd)):
    input_flux, angles, coeffs1, coeffs2 = pol_grating(
        0.5 * dd[k], math.radians(ph_uniaxial), gp, nmode
    )
    tran = (abs(coeffs1) ** 2 + abs(coeffs2) ** 2) / input_flux
    for m in range(nmode):
        print("tran (uniaxial):, {}, {:.2f}, {:.5f}".format(m, angles[m], tran[m]))
    m0_uniaxial[k] = tran[0]
    m1_uniaxial[k] = tran[1]
    ang_uniaxial[k] = angles[1]

    input_flux, angles, coeffs1, coeffs2 = pol_grating(
        dd[k], math.radians(ph_twisted), gp, nmode
    )
    tran = (abs(coeffs1) ** 2 + abs(coeffs2) ** 2) / input_flux
    for m in range(nmode):
        print("tran (twisted):, {}, {:.2f}, {:.5f}".format(m, angles[m], tran[m]))
    m0_twisted[k] = tran[0]
    m1_twisted[k] = tran[1]
    ang_twisted[k] = angles[1]