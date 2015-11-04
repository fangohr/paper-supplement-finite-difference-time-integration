import numpy as np
import matplotlib.pyplot as plt
from os import path
from fidimag.micro import Sim
from fidimag.common import CuboidMesh
from fidimag.micro import UniformExchange, Demag
from fidimag.micro import Zeeman, TimeZeeman
from fidimag.common.fileio import DataReader

mu0 = 4 * np.pi * 1e-7
A = 13e-12
MODULE_DIR = path.dirname(path.abspath(__file__))
INITIAL_MAGNETISATION_FILE = path.join(MODULE_DIR, "m0.npy")

def initial_magnetisation(mesh):
    sim = Sim(mesh, name='relax')

    sim.set_tols(rtol=1e-10, atol=1e-10)
    sim.alpha = 0.5
    sim.gamma = 2.211e5
    sim.Ms = 8.0e5
    sim.do_precession = False
    sim.set_m((1, 0.25, 0.1))
    sim.add(UniformExchange(A))
    sim.add(Demag())
    sim.relax(dt=1e-13, stopping_dmdt=0.01, max_steps=5000,
              save_m_steps=100, save_vtk_steps=50)
    np.save(INITIAL_MAGNETISATION_FILE, sim.spin)
    return sim.spin


def dynamics_field_1(mesh, initial_magnetisation):
    sim = Sim(mesh, name='dynamics_1')
    sim.set_tols(rtol=1e-10, atol=1e-10)
    sim.alpha = 0.02
    sim.gamma = 2.211e5
    sim.Ms = 8.0e5
    sim.set_m(initial_magnetisation)
    sim.add(UniformExchange(A))
    sim.add(Demag())

    mT = 0.001 / mu0
    zeeman = Zeeman([-24.6 * mT, 4.3 * mT, 0], name='H')
    sim.add(zeeman, save_field=True)

    ts = np.linspace(0, 1e-9, 201)
    for t in ts:
        sim.run_until(t)
        print 'sim t=%g' % t


def plot():
    data = DataReader('dynamics_1.txt')
    ts = data['time'] * 1e9
    mx = data['m_x']
    my = data['m_y']
    mz = data['m_z']

    plt.plot(ts, mx, '--', label='m_fidimag', dashes=(2, 2))
    plt.plot(ts, my, '--', label='', dashes=(2, 2))
    plt.plot(ts, mz, '--', label='', dashes=(2, 2))

    plt.title('standard problem 4')
    plt.legend()
    plt.xlabel('t (ns)')
    plt.ylabel('m (1)')
    plt.savefig('standard_problem_4.pdf')


if __name__ == '__main__':
    mesh = CuboidMesh(nx=200, ny=50, nz=1, dx=2.5, dy=2.5, dz=3, unit_length=1e-9)

    try:
        m0 = np.load(INITIAL_MAGNETISATION_FILE)
    except IOError:
        print "Couldn't find initial magnetisation at {}.".format(
                INITIAL_MAGNETISATION_FILE)
        print "Will run relaxation simulation."
        m0 = initial_magnetisation(mesh)

    dynamics_field_1(mesh, m0)
    plot()
