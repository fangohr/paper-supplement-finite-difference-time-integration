import os
import numpy as np
import matplotlib.pyplot as plt

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
OOMMF_DATAFILE = os.path.join(MODULE_DIR, "oommf", "std_4_dynamics_field_2.txt")

oommf_data = np.loadtxt(OOMMF_DATAFILE)
print oommf_data.shape

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(121)
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 2], label="mx")
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 3], label="my")
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 4], label="mz")
ax.set_xlim((0, 2))
ax.set_xlabel("time (ns)")
ax.set_ylim((-1, 1))
ax.set_ylabel("unit magnetisation (1)")
ax.legend()

ax = fig.add_subplot(122)
ax.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 1])
ax.set_xlim((0, 2))
ax.set_xlabel("time (ns)")
ax.set_ylabel("# of RHS evaluations")

fig.tight_layout()
fig.savefig("dynamics_evals.png")
