import meep as mp
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Video

resolution = 20
cell_size = mp.Vector3(14, 14)
pml_layers = [mp.PML(thickness=2)]

rot_angle = np.radians(20)
geometry = [
    mp.Block(
        center=mp.Vector3(),
        size=mp.Vector3(mp.inf, 1, mp.inf),
        e1=mp.Vector3(1, 0, 0),
        e2=mp.Vector3(0, 1, 0),
        material=mp.Medium(epsilon=12),
    )
]
fsrc = 0.15  # frequency of eigenmode or constant-amplitude source

sources = [
    mp.Source(
        src=mp.GaussianSource(fsrc, fwidth=0.2 * fsrc),
        center=mp.Vector3(),
        size=mp.Vector3(y=2),
        component=mp.Ez,
    )
]
sim = mp.Simulation(
    cell_size=cell_size,
    resolution=resolution,
    boundary_layers=pml_layers,
    sources=sources,
    geometry=geometry,
)

#plot the wave guide
f = plt.figure(dpi=100)
sim.plot2D(ax=f.gca())
plt.show()

#run the simulation for 50 timesteps after the source stops
#record every timestep
f = plt.figure(dpi=100)
animate = mp.Animate2D(sim, fields=mp.Ez, f=f, normalize=True)
sim.run(mp.at_every(1, animate), until_after_sources=50)
plt.close()

#video
filename = "oblique-source-normal.mp4"
animate.to_mp4(10, filename)
Video(filename)


