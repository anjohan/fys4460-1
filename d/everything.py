import tqdm
import os
import logplotter
import numpy as np
from units import units

Ts = np.linspace(2, 3.5, 11)
num_Ts = len(Ts)
Ps = np.zeros(num_Ts)
for k in tqdm.trange(num_Ts, desc="Running simulations: "):
    T = Ts[k]

    exit_code = os.system(
        "mpirun lmp_mpi -var T %g -in in.script > /dev/null" % T)
    if exit_code != 0:
        break

    data = logplotter.find_data("log.lammps")
    t = np.array(data["Time"]) * units.t0
    P = np.array(data["Press"]) * units.P0
    num_frames = len(t)
    if k == 0:
        skip = num_frames // 200
        np.savetxt("data/Pfirst.dat",
                   np.array([t[::skip], P[::skip]]).transpose())
    for i in range(num_frames):
        if abs(P[i] - P[-1]) < 0.5 * abs(P[i] - P[0]):
            break
    equilibrium_frames = 3 * i
    assert equilibrium_frames < 0.8 * num_frames,\
        "Longer simulation time required to reach equilibrium."
    Ps[k] = P[equilibrium_frames:].mean()

num_frames = len(t)
skip = num_frames // 200
np.savetxt("data/Plast.dat", np.array([t[::skip], P[::skip]]).transpose())

Ts = Ts[:k] * units.T0
Ps = Ps[:k]
np.savetxt("data/P.dat", np.array([Ts, Ps]).transpose())

np.savetxt("data/firstT.dat", [Ts[0]], fmt="%.3g")
np.savetxt("data/lastT.dat", [Ts[-1]], fmt="%.3g")
