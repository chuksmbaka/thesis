import meep as mp
import matplotlib.pyplot as plt
import numpy as np


a = 0.000001  # unit scale in meep
c = 299792458  # speed of light in a vacuum
resolution = 10
pml_x = 1.0
pml_y = 1.0

def freq_to_mp(frequency_in_hz):
    meep_freq = (frequency_in_hz * a)/c
    return meep_freq

def meter_to_mp(length_in_meters):
    aa = 1                                   # aa = 1 micro meter
    meep_length = length_in_meters/aa
    return meep_length

def sec_to_mp(time_in_secs):
    meep_time = time_in_secs*c/a
    return meep_time


#Computational Cell definition
x_axis = meter_to_mp(40)  # 30 micro meter
y_axis = meter_to_mp(20)  # 20 micro meter
cell = mp.Vector3(x_axis, y_axis, mp.inf)  # simulation cell size

#PML layer definition
pml_layer = [mp.PML(1.0)]

#medium definition
medium = mp.Medium(epsilon=12)  # Silicon

#Define the geometry of the guide
x_len = 20
y_width = 1
geometry = [ mp.Block(mp.Vector3(x_len, y_width, mp.inf), center=mp.Vector3(), material=medium,)]

#Source definition
compute_flux = False  # compute flux (True) or plot the field profile (False) **
eig_src = True  # eigenmode (True) or constant-amplitude (False) source
freq = freq_to_mp(150e12)  # frequency of 150THz

#################################################
eig_match_freq = True
######################################
sources = [
    mp.EigenModeSource(mp.ContinuousSource(frequency=freq), center=mp.Vector3(),
    size=mp.Vector3(y = 3*y_width), eig_band=1,)
]

#eig_src  = True
#Simulation of the setup
sim = mp.Simulation(
    cell_size=cell,
    resolution=resolution,
    boundary_layers=pml_layer,
    sources=sources,
    geometry=geometry,
)

sim.run(until_after_sources=10)
#sim.plot2D(
    #output_plane=mp.Volume(center=mp.Vector3(), size=mp.Vector3(x_axis, y_axis)), fields=mp.Ez,
#field_parameters={"alpha": 0.9},
   # )
#plt.show()
















