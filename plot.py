import os
import numpy as np
import matplotlib.pyplot as plt
from fidimag.common.fileio import DataReader  # for convenience

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
OOMMF_DATAFILE = os.path.join(MODULE_DIR, "oommf", "std_4_dynamics_field_2.txt")
FIDIMAG_DATAFILE = os.path.join(MODULE_DIR, "fidimag", "dynamics_1.txt")

oommf_data = np.loadtxt(OOMMF_DATAFILE)

# we could do np.loadtxt but wouldn't get header information
fidimag_data = DataReader(FIDIMAG_DATAFILE)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(121)
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 2], label="oommf mx")
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 3], label="oommf my")
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 4], label="oommf mz")
ax.plot(fidimag_data["time"] * 1e9, fidimag_data["m_x"], label="fidimag mx")
ax.plot(fidimag_data["time"] * 1e9, fidimag_data["m_y"], label="fidimag my")
ax.plot(fidimag_data["time"] * 1e9, fidimag_data["m_z"], label="fidimag mz")
ax.set_xlim((0, 2))
ax.set_xlabel("time (ns)")
ax.set_ylim((-1, 1))
ax.set_ylabel("unit magnetisation (1)")
ax.legend()

ax = fig.add_subplot(122)
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 1], label="oommf")
ax.plot(fidimag_data["time"] * 1e9, fidimag_data["rhs_evals"], label="fidimag")
ax.set_xlim((0, 2))
ax.set_xlabel("time (ns)")
ax.set_ylabel("# of RHS evaluations")
ax.legend()

fig.tight_layout()
fig.savefig("dynamics_evals.png")
