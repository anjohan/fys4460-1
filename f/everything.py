import tqdm
import os
import logplotter
import numpy as np
from units import units

Ts = np.linspace(1, 3., 5)
num_Ts = len(Ts)
Ds = np.zeros(num_Ts)

for i, T in enumerate(tqdm.tqdm(Ts, desc="Temperatures:".ljust(20))):
    os.system("mpirun lmp_mpi -var T %g -in in.script > /dev/null" % T)
    data = logplotter.find_data("data/log.msd_%g" % T)
