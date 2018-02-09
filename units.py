class UnitClass:
    def __init__(self):
        self.L0 = 3.405  # Å
        self.t0 = 2.1569E3  # fs
        self.E0 = 1.0318E-2  # eV
        self.F0 = self.E0/self.L0 # eV/Å
        self.T0 = 119.74  # K
        self.v0 = self.L0 / self.t0  # Å/fs
        self.P0 = self.F0 / (self.L0**2)  # eV/Å^2
        self.k_B = self.E0 / self.T0  # eV/K


units = UnitClass()
