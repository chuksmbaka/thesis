import meep as mp
import matplotlib.pyplot as plt

resolution = 10
x = 2
y = 5
z = 20

pml_layer = [mp.PML(thickness=1)]
cell_size = mp.Vector3(14, 30, 30)

material_shape = mp.Block(size=mp.Vector3(x, y, z), center=mp.Vector3(), material=mp.Medium(epsilon=12))
geometry = [material_shape]

f_max = 0.02
f_min = 0.01
df = f_max - f_min
center_f = 0.5 * (f_max + f_min)
source1 = mp.Source(mp.GaussianSource(frequency=center_f, fwidth=df), center=mp.Vector3(), size=mp.Vector3(x, y, z-10),
                    component=mp.Ex)
sources = [source1]

output_plane = mp.Volume(center=mp.Vector3(), size=mp.Vector3(x, 0, z))

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layer,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution,
                    k_point=mp.Vector3())
sim.run(until=100)
sim.plot2D(output_plane=output_plane, fields=mp.Ex)
plt.show()
