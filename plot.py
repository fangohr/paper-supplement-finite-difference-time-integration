import os
import numpy as np
import matplotlib.pyplot as plt
from fidimag.common.fileio import DataReader  # for convenience

plt.style.use("ggplot")


# input files and data from standard problem 4 field 2 simulations

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
OOMMF_DATAFILE = os.path.join(MODULE_DIR, "oommf", "std_4_dynamics_field_2.txt")
FIDIMAG_DATAFILE = os.path.join(MODULE_DIR, "fidimag", "dynamics_2.txt")
oommf_data = np.loadtxt(OOMMF_DATAFILE)
fidimag_data = DataReader(FIDIMAG_DATAFILE) # we could do np.loadtxt but wouldn't get header information


# LaTeX labels

math = lambda txt: "$" + txt + "$"  # concatenation because getting {{{}}}
rm = lambda txt: "\mathrm{" + txt + "}" # right in subsequent formats is hard
olbl = math(rm("oommf"))
flbl = math(rm("fidimag"))
lbli = lambda name, mi: math(rm(rm(name) + "\; m_" + rm(mi)))
olbli = lambda i: lbli("oommf", i)
flbli = lambda i: lbli("fidimag", i)


# plotting

fig, (ax1, ax2) = plt.subplots(2, figsize=(10, 8), sharex=True)

ax1.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 2], "b-", label=olbli("x"))
ax1.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 3], "g-", label=olbli("y"))
ax1.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 4], "r-", label=olbli("z"))
ax1.plot(fidimag_data["time"] * 1e9, fidimag_data["m_x"], "bx", label=flbli("x"))
ax1.plot(fidimag_data["time"] * 1e9, fidimag_data["m_y"], "gx", label=flbli("y"))
ax1.plot(fidimag_data["time"] * 1e9, fidimag_data["m_z"], "rx", label=flbli("z"))
ax1.set_xlim((0, 2))
ax1.set_ylim((-1.05, 1))
ax1.set_ylabel("unit magnetisation (1)")
ax1.legend()
ax1.set_title("Standard Problem 4 Field 2")

ax2.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 1], "r", label=olbl)
ax2.plot(fidimag_data["time"] * 1e9, fidimag_data["rhs_evals"], "g", label=flbl)
ax2.set_xlim((0, 2))
ax2.set_xlabel("time (ns)")
ax2.set_ylabel("# of RHS evaluations")
ax2.legend()

fig.tight_layout()
fig.savefig("dynamics_evals.png")
