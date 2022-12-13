import meep as mp

resolution = 10


def ring_resonator(p):
    rr = (p.x ** 2 + p.y ** 2) ** 0.5
    if (rr > rad) and (rr < rad + W):
        print("rad is: ", rad)
        return mp.Medium(index=n)
    return mp.air


ring_resonator.do_averaging = True
geometry = [mp.Block(center=mp.Vector3(), size=mp.Vector3(5, 5), material=ring_resonator)]

sim = mp.Simulation(cell_size=mp.Vector3(5, 5), geometry=geometry, subpixel_tol=1e-4, subpixel_maxeval=1000,
                    resolution=resolution, boundary_layers=[mp.PML(1)])
