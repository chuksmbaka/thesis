import meep as mp
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Video


def func():
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

    kx = 1  # initial wavevector guess in x direction of the eigenmode
    kpoint = mp.Vector3(x=kx)
    bnum = 2  # band number of the eigenmode

    sources = [
        mp.EigenModeSource(
            src=mp.ContinuousSource(fsrc, fwidth=0.2 * fsrc),
            center=mp.Vector3(-5),
            size=mp.Vector3(y=2),
            direction=mp.NO_DIRECTION,
            eig_kpoint=kpoint,
            eig_band=bnum,
            # eig_parity=mp.EVEN_Y + mp.ODD_Z if rot_angle == 0 else mp.ODD_Z,
            eig_match_freq=True,
        )
    ]

    sim = mp.Simulation(
        cell_size=cell_size,
        resolution=resolution,
        boundary_layers=pml_layers,
        sources=sources,
        geometry=geometry,
        # symmetries=[mp.Mirror(mp.Y, phase=-1)]
    )

    # Define xy plane
    # output_plane = mp.Volume(center=mp.Vector3(), size=mp.Vector3(3, 1))
    # f = plt.figure(dpi=100)
    # animate = mp.Animate2D(sim, mp.Ez, f=f, normalize=True, output_plane=output_plane, realtime=True)
    # animate = mp.Animate2D(sim, mp.Ez, normalize=True, output_plane=output_plane, realtime=True)
    animate = mp.Animate2D(sim, mp.Ez, normalize=True, realtime=True)
    sim.run(mp.at_every(0.5, animate), until=100)
    # sim.plot2D(output_plane=output_plane, fields=mp.Ez)
    sim.plot2D(fields=mp.Ez)
    plt.savefig('plane_wave_{:}.png'.format('Ez_in_xy_plane'))
    plt.show()
    plt.close()


# filename = "oblique-source-eigcw.mp4"
# animate.to_mp4(10, filename)
# Video(filename)

    filename = "2d_animation.gif"
    animate.to_gif(5, filename)


if __name__ == '__main__':
    func()