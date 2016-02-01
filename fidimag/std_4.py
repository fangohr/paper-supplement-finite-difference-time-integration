import time
import numpy as np
import matplotlib.pyplot as plt
from os import path
from math import sqrt
from fidimag.common import CuboidMesh
from fidimag.common.fileio import DataReader
from fidimag.micro import Sim, Demag, UniformExchange, Zeeman, TimeZeeman

MODULE_DIR = path.dirname(path.abspath(__file__))
M0_FILE = path.join(MODULE_DIR, "m0.npy")  # initial state

mu0 = 4 * np.pi * 1e-7
mT = 1e-3 / mu0
A = 13e-12
Ms = 8.0e5
alpha = 0.02
gamma = 2.211e5


def setup_simulation(mesh, m0, simulation_name, integrator="sundials"):
    sim = Sim(mesh, name=simulation_name, integrator=integrator)
    sim.set_m(m0)
    sim.Ms = Ms
    sim.alpha = alpha
    sim.gamma = gamma
    sim.add(UniformExchange(A))
    sim.add(Demag())
    return sim


def get_initial_state(mesh):
    sim = setup_simulation(mesh, (1, 0.25, 0.1), "relaxation")
    H0 = [Ms / sqrt(3) for _ in xrange(3)]
    Ht = lambda t: 1 - t / 0.5e-9 if t < 0.5e-9 else 0
    sim.add(TimeZeeman(H0, Ht))  # saturating field H0 * H(t)
    sim.do_precession = False
    sim.set_tols(rtol=1e-10, atol=1e-10)
    sim.relax(stopping_dmdt=0.01, max_steps=5000)
    return sim.spin


def run_dynamics(mesh, initial_state, integrator_settings):
    if integrator_settings[0] == "sundials":
        integrator, rtol, atol = integrator_settings
        print "Simulation with sundials integrator, rtol={}, atol={}.".format(rtol, atol)
        sim = setup_simulation(mesh, initial_state, "dyn_r{}_a{}".format(rtol, atol), integrator)
        sim.set_tols(rtol=rtol, atol=atol)
    else:
        integrator, stepsize = integrator_settings
        print "Simulation with {} integrator, stepsize={}.".format(integrator, stepsize)
        sim = setup_simulation(mesh, initial_state, "dyn_{}_h{}".format(integrator, stepsize), integrator)
        sim.integrator.h = stepsize
    sim.add(Zeeman([-35.5 * mT, -6.3 * mT, 0], name='H'), save_field=True)

    ts = np.linspace(0, 2e-9, 501)
    for ti, t in enumerate(ts):
        sim.run_until(t)
        if ti % 100 == 0:
            print "it's {} now, simulated {} s.".format(time.strftime("%d/%m/%Y %H:%M:%S"), t)


def run(integrator_settings):
    mesh = CuboidMesh(nx=500, ny=125, nz=3, dx=1, dy=1, dz=1, unit_length=1e-9)
    try:
        m0 = np.load(M0_FILE)
    except IOError:
        print "No initial state at {}. Running relexation.".format(M0_FILE)
        m0 = get_initial_state(mesh)
        np.save(M0_FILE, m0)
    run_dynamics(mesh, m0, integrator_settings)

if __name__ == "__main__":
    for tol in xrange(5, 11):
        run(("sundials", tol, tol))
    run(("euler", 1e-14))
    run(("euler", 1e-12))
    run(("rk4", 1e-14))
    run(("rk4", 1e-12))
