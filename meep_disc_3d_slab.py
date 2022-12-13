import meep as mp
import matplotlib.pyplot as plt
cell_len = 5


def anim_plane_wave(polarization, plane, title):
    resolution = 5
    dpml = 1

    pml_layers = [mp.PML(thickness=dpml)]
    cell_size = mp.Vector3(cell_len, cell_len, cell_len)
    source_com = polarization

    sources = [mp.Source(mp.GaussianSource(1, fwidth=0.25),
                         center=mp.Vector3(dpml - cell_len/2),
                         size=mp.Vector3(0, cell_len, cell_len),
                         component=source_com)]

    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=pml_layers,
                        sources=sources,
                        k_point=mp.Vector3())

    output_plane = mp.Volume(center=mp.Vector3(), size=mp.Vector3(plane[0], plane[1], plane[2]))
    anim = mp.Animate2D(sim,
                        fields=source_com,
                        normalize=True,
                        output_plane=output_plane,
                        realtime=True)

    sim.run(mp.at_every(1, anim), until=20)
    sim.plot2D(output_plane=output_plane,fields=source_com)
    plt.savefig('plane_wave_{:}.png'.format(title))
    plt.close()

if __name__ == '__main__':
    anim_plane_wave(polarization=mp.Ey, plane=[cell_len, 0, cell_len], title='Ey_xz')
    anim_plane_wave(polarization=mp.Ey, plane=[cell_len, cell_len, 0], title='Ey_xy')
    anim_plane_wave(polarization=mp.Ez, plane=[cell_len, 0, cell_len], title='Ez_xz')
    anim_plane_wave(polarization=mp.Ez, plane=[cell_len, cell_len, 0], title='Ez_xy')