import time
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
smallest_error = float("inf")
a, b = 0, 0
t0 = time.time()
while time.time() - t0 < 600:
    a0, b0 = np.random.uniform(1E-10, 10, size=2)
    params, covariancestuff = curve_fit(
        vanderWaal, [rhos, equilibrium_Ts.ravel()], flat_Ps, p0=(a0, b0))

    atmp, btmp = params
    computed_Ptmp = vanderWaal([rhos, equilibrium_Ts.ravel()], atmp, btmp)
    absolute_errortmp = np.abs((computed_Ptmp - flat_Ps))
    error = np.sum(absolute_errortmp)
    print("Trying a0 = %8g, b0 = %8g, result: a = %8g, b = %8g, error = %8g" %
          (a0, b0, atmp, btmp, error))
    if error < smallest_error:
        smallest_error = error
        a, b = atmp, btmp
        computed_P = computed_Ptmp
        absolute_error = absolute_errortmp

relative_error = np.abs(absolute_error / flat_Ps)

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

np.savetxt("data/simulatedPs.dat", Ps)
np.savetxt("data/fittedPs.dat", computed_P.reshape((num_rhos, num_Ts)))
np.savetxt("data/eqTs.dat", equilibrium_Ts)
