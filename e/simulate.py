from tqdm import trange
import os
import numpy as np

rhos = np.linspace(0.01, 1, 30)
Ts = np.linspace(1, 3.0, 10)

np.savetxt("data/rhos.dat", rhos)
np.savetxt("data/Ts.dat", Ts)

for i in trange(len(rhos), desc="Densities:".ljust(20)):
    for j in trange(len(Ts), desc="Temperatures:".ljust(20)):
        os.system("make data/log.%g_%g > /dev/null" % (rhos[i], Ts[j]))
print()
