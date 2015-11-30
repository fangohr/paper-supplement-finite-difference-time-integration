import os
import numpy as np
import matplotlib.pyplot as plt
from fidimag.common.fileio import DataReader  # for convenience

plt.style.use("ggplot")

# input files and data from standard problem 4 field 2 simulations

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
OOMMF_DATAFILE = os.path.join(MODULE_DIR, "oommf", "std_4_dynamics_field_2.txt")
FIDIMAG_DATAFILE = os.path.join(MODULE_DIR, "fidimag", "dyn_r{0}_a{0}.txt")
fidimag_tols = (1e-6, 1e-8, 1e-10)
oommf_data = np.loadtxt(OOMMF_DATAFILE)


# LaTeX labels

math = lambda txt: "$" + txt + "$"  # concatenation because getting {{{}}}
rm = lambda txt: "\mathrm{" + txt + "}" # right in subsequent formats is hard
olbl = math(rm("oommf"))
flbl = math(rm("fidimag"))
lbli = lambda name, mi: math(rm(rm(name) + "\; m_" + rm(mi)))
olbli = lambda i: lbli("oommf", i)
flbli = lambda i: lbli("fidimag", i)


# plotting

# showing averages

fig, axes = plt.subplots(3, figsize=(10, 8), sharex=True)
axes[2].set_xlabel("time (ns)")
axes[2].set_xlim((0, 2))

for i, tol in enumerate(fidimag_tols):
    fidimag_data = DataReader(FIDIMAG_DATAFILE.format(tol))
    axes[i].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 2], "b-", label=olbli("x"))
    axes[i].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 3], "g-", label=olbli("y"))
    axes[i].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 4], "r-", label=olbli("z"))
    axes[i].plot(fidimag_data["time"] * 1e9, fidimag_data["m_x"], "bx", label=flbli("x"))
    axes[i].plot(fidimag_data["time"] * 1e9, fidimag_data["m_y"], "gx", label=flbli("y"))
    axes[i].plot(fidimag_data["time"] * 1e9, fidimag_data["m_z"], "rx", label=flbli("z"))
    axes[i].set_ylim((-1.05, 1))
    axes[i].set_ylabel("unit magnetisation (1)")
    axes[i].legend()
    axes[i].set_title("tol {}".format(tol))

fig.tight_layout()
fig.savefig("dynamics.png")
plt.close(fig)

# difference of averages between oommf and finmag

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
ax2.set_xlabel("time (ns)")
ax2.set_xlim((0, 2))

differences = [] # differences between oommf and given fidimag tol

for i, tol in enumerate(fidimag_tols):
    fidimag_data = DataReader(FIDIMAG_DATAFILE.format(tol))
    if tol == 1e-8:
        difference = np.sqrt((oommf_data[:105, 2] - fidimag_data["m_x"]) ** 2 +
                             (oommf_data[:105, 3] - fidimag_data["m_y"]) ** 2 +
                             (oommf_data[:105, 4] - fidimag_data["m_z"]) ** 2)
        #axis.plot(fidimag_data["time"] * 1e9, 2 * difference, label=str(tol))
    else:
        difference = np.sqrt((oommf_data[:, 2] - fidimag_data["m_x"]) ** 2 +
                             (oommf_data[:, 3] - fidimag_data["m_y"]) ** 2 +
                             (oommf_data[:, 4] - fidimag_data["m_z"]) ** 2)
        differences.append(difference)
        ax1.plot(fidimag_data["time"] * 1e9, difference, label=str(tol))


ax2.plot(fidimag_data["time"] * 1e9, differences[1] - differences[0])
ax1.set_title("$\mathrm{difference\; to\; oommf}$")
ax2.set_title("$\mathrm{difference\; of\; difference}$")  # ...
ax1.set_ylabel("deviance (1)")
ax2.set_ylabel("difference (1)")
ax1.legend()
fig.tight_layout()
fig.savefig("difference.png")
plt.close(fig)

# number of RHS evaluations

fig, axis = plt.subplots()
axis.set_xlabel("time (ns)")
axis.set_xlim((0, 2))
axis.set_ylabel("# of RHS evaluations")

axis.plot(oommf_data[:, 0] * 1e9, oommf_data[:, 1], "r", label=olbl)

for tol in fidimag_tols:
    fidimag_data = DataReader(FIDIMAG_DATAFILE.format(tol))
    axis.plot(fidimag_data["time"] * 1e9, fidimag_data["rhs_evals"], label=flbl + "$\,{}$".format(tol))

axis.legend()
fig.savefig("work.png")
plt.close(fig)
