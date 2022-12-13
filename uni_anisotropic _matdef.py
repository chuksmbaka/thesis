import meep as mp
import matplotlib.pyplot as plt
import numpy as np

resolution = 10
pml_layer = [mp.PML(thickness=1)]
cell = mp.Vector3(16, 8, 0)


#################################### material definition ##########################################


def LiN(p):
    eps_o = 3
    eps_e = 12
    ln_epsilon = mp.Matrix(mp.Vector3(eps_o, 0, 0), mp.Vector3(0, eps_e, 0), mp.Vector3(0, 0, eps_o))
    ln_epsilon_diag = mp.Vector3(ln_epsilon[0].x, ln_epsilon[1].y, ln_epsilon[2].z)
    return mp.Medium(epsilon_diag=ln_epsilon_diag)


###################################################################################################

geometry = [mp.Block(center=mp.Vector3(), size=mp.Vector3(mp.inf, 1, mp.inf), material=LiN)]
sources = [
    mp.Source(
        mp.ContinuousSource(frequency=0.15), component=mp.Ez, center=mp.Vector3(-7, 0), size=mp.Vector3(0, 1, 0)
    )
]

sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layer,
                    geometry=geometry,
                    resolution=resolution,
                    sources=sources)
sim.run(until=100)

eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)

#############################################   to be removed  #########################################


print("variable type of eps_datas: ", type(eps_data))
print("shape of eps data: ", np.shape(eps_data))
print("sample data: ", eps_data[:, :])
file = open("eps_data.txt", "w")
eps_dat = str(eps_data)
for i in eps_dat:
    file.write(i)
file.close()

##############################################################################################

plt.figure(dpi=100)
plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
# plt.axis('off')
plt.show()

ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.imshow(ez_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
plt.axis("off")
plt.show()

##################################### Animation #######################################################

sim.reset_meep()
f = plt.figure(dpi=100)
Animate = mp.Animate2D(sim, fields=mp.Ez, f=f, realtime=False, normalize=True)
plt.close()

sim.run(mp.at_every(1, Animate), until=100)
plt.close()

filename = "uniaxial_ani_mat.mp4"
Animate.to_mp4(10, filename)

from IPython.display import Video

Video(filename)

###############################################################################################
