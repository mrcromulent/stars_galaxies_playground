import matplotlib.pyplot as plt
from mesa_data import MesaData
import numpy as np


def main():
    mstr = ["1", "10", "100"]

    for i, mass in enumerate([1.0, 10.0, 100.0]):

        md = MesaData(f"../mesa_models/M{mstr[i]}Z001")

        x = np.log10(md.df["star_age"])
        y1 = md.df["log_L"]
        y2 = md.df["pp"]
        y3 = md.df["cno"]
        y4 = md.df["tri_alfa"]
        sm = np.log10(10 ** y1 + 10 ** y2 + 10 ** y3 + 10 ** y4)

        fig, ax = plt.subplots()
        ax.plot(x, y1, label="Luminosity")
        ax.plot(x, y2, label="PP")
        ax.plot(x, y3, label="CNO")
        ax.plot(x, y4, label="Triple Alpha")
        ax.plot(x, sm, label="Sum")
        ax.set_title(f'Surface Luminosity  over stellar lifetime (M = {md.m})')
        ax.set_xlabel('log(Stellar age) [yrs]')
        ax.set_ylabel('log(Luminosity) [L_(sol)]')
        ax.legend()
        fig.show()
        # fig.savefig(f"../figs/surface_luminosity_evolution_m={mass}.png", dpi=300)


if __name__ == "__main__":
    main()
