import matplotlib.pyplot as plt
from mesa_data import MesaData
from glob import glob


def main():
    cols = {0.01: "r",
            0.0001: "b"}

    ages = [1e6, 1e7, 1e8, 1e9, 1e10]
    age_labels = ["ok", "sk", "^k", "hk", "*k"]

    #
    fig, ax = plt.subplots()
    ax.set_title('Hertzsprung-Russell Diagram for Metallicities Z = 0.01 and Z = 0.0001')
    ax.set_ylabel('log(Luminosity) [L_(sol)]')
    ax.set_xlabel('log(T_eff) [K]')
    for direc in glob("../mesa_models/M*Z*"):
        md = MesaData(direc)

        x = md.df["log_Teff"]
        y = md.df["log_L"]

        #
        ax.plot(x,
                y,
                markersize=1,
                marker=".",
                color=cols[md.z],
                label=f"{md.z}")

        #
        for i, age in enumerate(ages):
            idx = md.first_idx_of_age(age)
            if idx is not None:
                mrkr = age_labels[i]
                ax.plot(x[idx], y[idx], mrkr, label=f"Age = {age:.1E}")

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    ax.invert_xaxis()
    fig.show()
    # fig.savefig("../figs/hr_trajectories.png", dpi=300)


if __name__ == "__main__":
    main()
