from units import units
import logplotter
import tqdm
import numpy as np
from scipy.optimize import curve_fit

rhos = np.loadtxt("data/rhos.dat")
Ts = np.loadtxt("data/Ts.dat")

num_rhos = len(rhos)
num_Ts = len(Ts)

Ps = np.zeros((num_rhos, num_Ts))

for i, rho in enumerate(tqdm.tqdm(rhos, desc="Densities:".ljust(20))):
    for j, T in enumerate(tqdm.tqdm(Ts, desc="Temperatures:".ljust(20))):
        data = logplotter.find_data("data/log.%g_%g" % (rho, T))
        P = data["Press"]
        T = data["Temp"]
        num_frames = len(P)
        k = 0
        while abs(T[-1] - T[k]) > 0.5 * abs(T[0] - T[-1]):
            k += 1
        equilibrium_index = 4 * k
        assert equilibrium_index < 0.8 * \
            num_frames, "Longer simulation needed for rho=%g, T=%g" % (rho, T)
        Ps[i, j] = np.mean(P[equilibrium_index:])

# rhos /= units.L0**3
# Ts *= units.T0
# Ps *= units.P0
flat_Ps = Ps.ravel()
print()


def vanderWaal(rhos_and_Ts, a, b):
    rhos, Ts = rhos_and_Ts
    num_rhos, num_Ts = len(rhos), len(Ts)
    Ps = np.zeros((num_rhos, num_Ts))
    for i, rho in enumerate(rhos):
        for j, T in enumerate(Ts):
            Ps[i, j] = rho**2 * (T / (1 - rho * b) - a)
    return Ps.ravel()


print("Finding parameters...")
params, covariancestuff = curve_fit(vanderWaal, [rhos, Ts], flat_Ps)

a, b = params
print("a = %g, b = %g" % (a, b))
computed_P = vanderWaal([rhos, Ts], a, b)
relative_error = np.abs((computed_P - flat_Ps) / flat_Ps)

for filename, values in (("fitted.dat", computed_P.reshape(
    (num_rhos, num_Ts))), ("simulated.dat", Ps), ("relative_error.dat",
                                                  relative_error.reshape(
                                                      (num_rhos, num_Ts)))):
    with open("data/" + filename, "w") as outfile:
        for j, T in enumerate(Ts):
            for i, rho in enumerate(rhos):
                outfile.write("%g %g %g\n" % (rho, T, values[i, j]))
            outfile.write("\n")
