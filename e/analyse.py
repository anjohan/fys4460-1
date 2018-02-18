import pdb
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
equilibrium_Ts = np.zeros_like(Ps)

for i, rho in enumerate(tqdm.tqdm(rhos, desc="Densities:".ljust(20))):
    for j, T in enumerate(tqdm.tqdm(Ts, desc="Temperatures:".ljust(20))):
        data = logplotter.find_data("data/log.%g_%g" % (rho, T))
        P = data["Press"]
        T = data["Temp"]
        num_frames = len(P)
        k = 0
        initial_deviation = max(
            map(lambda x: abs(x - T[-1]), T[:num_frames // 10]))
        while abs(T[-1] - T[k]) > 0.5 * initial_deviation:
            k += 1
        equilibrium_index = 3 * k
        assert equilibrium_index < num_frames,\
            "Longer simulation needed for rho=%g, T=%g" % (rho, Ts[j])
        Ps[i, j] = np.mean(P[equilibrium_index:])
        equilibrium_Ts[i, j] = np.mean(T[equilibrium_index:])

# rhos /= units.L0**3
# Ts *= units.T0
# Ps *= units.P0
flat_Ps = Ps.ravel()
print()


def vanderWaal(rhos_and_Ts, a, b):
    rhos, Ts = rhos_and_Ts
    num_rhos = len(rhos)
    num_Ts = int(len(Ts) / len(rhos))
    Ts = Ts.reshape((num_rhos, num_Ts))
    Ps = np.zeros_like(Ts)
    # pdb.set_trace()
    for i, rho in enumerate(rhos):
        for j in range(num_Ts):
            Ps[i, j] = rho * Ts[i, j] / (1 - rho * b) - a * rho**2
    return Ps.ravel()


print("Finding parameters...")
params, covariancestuff = curve_fit(
    vanderWaal, [rhos, equilibrium_Ts.ravel()], flat_Ps, p0=(1.2, 0.1))
print(params, covariancestuff)

a, b = params
print("a = %g, b = %g" % (a, b))
computed_P = vanderWaal([rhos, equilibrium_Ts.ravel()], a, b)
relative_error = np.abs((computed_P - flat_Ps) / flat_Ps)

for filename, values in (("fitted.dat", computed_P.reshape(
    (num_rhos, num_Ts))), ("simulated.dat", Ps), ("relative_error.dat",
                                                  relative_error.reshape(
                                                      (num_rhos, num_Ts)))):
    with open("data/" + filename, "w") as outfile:
        for j in range(num_Ts):
            for i, rho in enumerate(rhos):
                outfile.write("%g %g %g\n" % (rho, equilibrium_Ts[i, j],
                                              values[i, j]))
            outfile.write("\n")
np.savetxt("data/a.dat", [a], fmt="%g")
np.savetxt("data/b.dat", [b], fmt="%g")
