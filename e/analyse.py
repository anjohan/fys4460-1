from units import units
import logplotter
import tqdm
import numpy as np

rhos = np.loadtxt("data/rhos.dat")
Ts = np.loadtxt("data/Ts.dat")

num_rhos = len(rhos)
num_Ts = len(Ts)

Ps = np.zeros((num_rhos, num_Ts))

for i, rho in enumerate(tqdm.tqdm(rhos, desc="Densities:".ljust(20))):
    for j, T in enumerate(tqdm.tqdm(Ts, desc="Temperatures:".ljust(20))):
        data = logplotter.find_data("data/log.%g_%g", rho, T)
        P = data["Press"]
