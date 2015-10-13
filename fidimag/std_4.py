import numpy as np
import matplotlib.pyplot as plt
from fidimag.micro import Sim
from fidimag.micro import FDMesh
from fidimag.micro import UniformExchange, Demag
from fidimag.micro import Zeeman, TimeZeeman
from fidimag.common.fileio import DataReader

mu0 = 4 * np.pi * 1e-7
A = 13e-12


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
    np.save('m0.npy', sim.spin)


def dynamics_field_1(mesh):
    sim = Sim(mesh, name='dynamics_1')
    sim.set_tols(rtol=1e-10, atol=1e-10)
    sim.alpha = 0.02
    sim.gamma = 2.211e5
    sim.Ms = 8.0e5
    sim.set_m(np.load('m0.npy'))
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
    mesh = FDMesh(nx=200, ny=50, nz=1, dx=2.5, dy=2.5, dz=3, unit_length=1e-9)
    initial_magnetisation(mesh)
    dynamics_field_1(mesh)
    plot()
