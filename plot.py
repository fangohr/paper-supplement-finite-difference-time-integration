import glob
import numpy as np
import os
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fidimag.common.fileio import DataReader  # for convenience

plt.style.use("ggplot")

# input files and data from standard problem 4 field 2 simulations
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
OOMMF_DATAFILE = os.path.join(MODULE_DIR, "oommf", "std_4_dynamics_field_2.txt")
FIDIMAG_DATAFILES = sorted(glob.glob(os.path.join(MODULE_DIR, "fidimag", "dyn_r*_a*.txt")))
oommf_data = np.loadtxt(OOMMF_DATAFILE)

#FIXME: oommf magnetisation data is recorded between t = 4e-12 and t = 2.004e-9
# whereas fidimag data is recorded between t = 0 and t = 2e-9 (as it should be)
# that explains the slight discrepancy (?)

# LaTeX labels
math = lambda txt: "$" + txt + "$"      # concatenation because getting {{{}}}
rm = lambda txt: "\mathrm{" + txt + "}" # right in subsequent formats is hard
olbl = math(rm("oommf"))
flbl = math(rm("fidimag"))
lbli = lambda name, mi: math(rm(rm(name) + "\; m_" + rm(mi)))
olbli = lambda i: lbli("oommf", i)
flbli = lambda i: lbli("fidimag", i)

for fi in FIDIMAG_DATAFILES:
    data = DataReader(fi)
    tol = re.search('dyn_r([0-9]+)_a', fi).groups()[0]  # get exponent from filename
    difference = np.sqrt((oommf_data[:, 2] - data["m_x"]) ** 2 +
                         (oommf_data[:, 3] - data["m_y"]) ** 2 +
                         (oommf_data[:, 4] - data["m_z"]) ** 2)

    fig, axes = plt.subplots(3, figsize=(10, 8), sharex= True)

    # dynamics of average magnetisation plotted
    axes[0].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 2], "b-", label=olbli("x"))
    axes[0].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 3], "g-", label=olbli("y"))
    axes[0].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 4], "r-", label=olbli("z"))
    axes[0].plot(data["time"] * 1e9, data["m_x"], "bx", label=flbli("x"))
    axes[0].plot(data["time"] * 1e9, data["m_y"], "gx", label=flbli("y"))
    axes[0].plot(data["time"] * 1e9, data["m_z"], "rx", label=flbli("z"))
    axes[0].set_ylim((-1.05, 1))
    axes[0].set_ylabel("unit magnetisation (1)")
    axes[0].legend()
    axes[0].set_title("tol 1e-{}".format(tol))

    # difference of average magnetisations between oommf and finmag
    axes[1].plot(data["time"] * 1e9, difference, label=str(tol))
    axes[1].set_ylabel("difference")

    # number of RHS evaluations
    axes[2].plot(oommf_data[:, 0] * 1e9, oommf_data[:, 1], "r", label=olbl)
    axes[2].plot(data["time"] * 1e9, data["rhs_evals"], label=flbl + "$\,1e-{}$".format(tol))
    axes[2].legend()
    axes[2].set_ylabel("# of RHS evaluations")
    axes[2].set_xlabel("time (ns)")
    axes[2].set_xlim((0, 2))

    fig.tight_layout()
    fig.savefig("dynamics_r{}.png".format(tol))
    plt.close(fig)
