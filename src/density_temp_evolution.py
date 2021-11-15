import matplotlib.pyplot as plt
from mesa_data import MesaData
from glob import glob


def main():
    zstr = ["001", "00001"]

    for i, z in enumerate([0.001, 0.0001]):

        fig, ax = plt.subplots()
        for direc in sorted(glob(f"../mesa_models/M*Z{zstr[i]}")):
            md = MesaData(direc)
            ax.plot(md.df["log_center_Rho"],
                    md.df["log_center_T"],
                    marker=".",
                    label=f"M = {round(md.m, 2)}",
                    markersize=1)

        ax.plot([-2.50, 4.00], [7.50, 6.50], color="orange", label="H flash")
        ax.plot([+0.00, 7.00], [8.50, 8.00], color="blue", label="He flash")
        ax.plot([+2.50, 8.00], [8.75, 8.50], color="black", label="Carbon flash")

        ax.set_title(f'Temporal Evolution of Central Density vs Central Temperature (Z = {z})')
        ax.set_xlabel('log(Central Density) [g/cm^3]')
        ax.set_ylabel('log(Central Temperature) [K]')
        ax.legend()
        fig.show()
        # fig.savefig(f"../figs/rho_temp_z={z}.png", dpi=300)


if __name__ == "__main__":
    main()
