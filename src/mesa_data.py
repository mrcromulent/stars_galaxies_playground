import pandas as pd
import re
import os


class MesaData:

    def __init__(self, dirname):

        self.data_file = os.path.join(dirname, "trimmed_history.data")
        dn = os.path.basename(os.path.normpath(dirname))
        m_str = re.findall(r"(?<=M)[\d]*", dn)[0]
        z_str = re.findall(r"(?<=Z)0*[\d]", dn)[0]

        leading_zeros = len(m_str) - len(m_str.lstrip("0"))
        self.m = float(m_str) * 10 ** (- leading_zeros)

        leading_zeros = len(z_str) - len(z_str.lstrip("0"))
        self.z = float(z_str) * 10 ** (- leading_zeros)

        print(f"{dn=}, {self.m=}, {self.z=}")

        self.df = pd.read_csv(self.data_file, skiprows=5,
                              delim_whitespace=True,
                              usecols=["star_age",
                                       "star_mass",
                                       "log_L",
                                       "log_Teff",
                                       "log_R",
                                       "log_center_T",
                                       "log_center_Rho",
                                       "pp",
                                       "cno",
                                       "tri_alfa",
                                       "center_h1"])

    def first_idx_of_age(self, age):
        res = self.df["star_age"].gt(age)

        if not res.any():
            return None
        else:
            return self.df["star_age"][res].index[0]

    def extract_data_at_mass_fraction(self, mass_fraction):
        res = self.df["center_h1"].lt(mass_fraction)
        idx = self.df["center_h1"][res].index[0]
        return self.df.iloc[idx]
