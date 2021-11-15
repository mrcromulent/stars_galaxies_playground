import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from mesa_data import MesaData
from glob import glob
import numpy as np


def plot(x, y, col, quant, ax):
    bf1, res1, _, _, _ = np.polyfit(x, y, 1, full=True)

    # Top row shows complete plot
    ax.plot(x,
            y,
            linestyle="None",
            color=col,
            marker=".")

    #
    fx = np.unique(x)
    fy = np.poly1d(bf1)(fx)
    ax.plot(fx, fy, col,
            label=f"slope={bf1[0]:.2}, Residual={res1[0]:.2}")
    ax.set_xlabel("log(Mass) [M_(sol)]")
    ax.set_ylabel(f"{quant}")
    ax.legend(prop={'size': 7})


def main():

    target_mf = 0.65
    m_cutoff = 3.0

    data = {
        0.0001:
            {
                "col":      "b",
                "log_R":    [],
                "log_M":    [],
                "log_L":    [],
                "log_Teff": []
            },
        0.01:
            {
                "col": "r",
                "log_R": [],
                "log_M": [],
                "log_L": [],
                "log_Teff": []
            },
        }

    for direc in glob("../mesa_models/M*Z*"):
        md = MesaData(direc)

        df_row = md.extract_data_at_mass_fraction(target_mf)
        data[md.z]["log_R"].append(df_row["log_R"])
        data[md.z]["log_L"].append(df_row["log_L"])
        data[md.z]["log_Teff"].append(df_row["log_Teff"])
        data[md.z]["log_M"].append(np.log10(md.m))

    # print(data)

    for i, quant in enumerate(["log_L", "log_Teff", "log_R"]):

        fig = plt.figure(i)
        gs = gridspec.GridSpec(2, 2)

        for j, z in enumerate([0.01, 0.0001]):

            plot_col = data[z]["col"]

            # Plot the top row
            ax = plt.subplot(gs[0, :])
            x = data[z]["log_M"]
            y = data[z][quant]
            plot(x, y, plot_col, quant, ax)
            ax.set_title(f"Value when central H abundance falls below: {target_mf}")

            # Bottom row shows the fits for the points on either side of the cutoff

            # M < m_cutoff
            ax = plt.subplot(gs[1, 0])

            xarr = np.array(data[z]["log_M"])
            yarr = np.array(data[z][quant])
            x = xarr[np.where(xarr < np.log10(m_cutoff))]
            y = yarr[np.where(xarr < np.log10(m_cutoff))]

            plot(x, y, plot_col, quant, ax)
            ax.set_title(f"Mass < {m_cutoff}")

            # M > m_cutoff
            ax = plt.subplot(gs[1, 1])

            xarr = np.array(data[z]["log_M"])
            yarr = np.array(data[z][quant])
            x = xarr[np.where(xarr > np.log10(m_cutoff))]
            y = yarr[np.where(xarr > np.log10(m_cutoff))]
            plot(x, y, plot_col, quant, ax)
            ax.set_title(f"Mass > {m_cutoff}")

        fig.tight_layout()
        fig.show()
        # fig.savefig(f"../figs/{quant}_fit.png", dpi=300)


if __name__ == "__main__":
    main()
