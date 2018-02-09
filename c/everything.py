import tqdm
import os
import logplotter
import numpy as np
from units import units

sizes = np.arange(5, 16, 1)
num_sizes = len(sizes)
stddev = np.zeros(num_sizes)
T0 = 2.5
for k in tqdm.trange(num_sizes, desc="Running simulations: "):
    size = sizes[k]

    exit_code = os.system(
        "mpirun lmp_mpi -var size %g -var T0 %g -in in.script > /dev/null" %
        (size, T0))
    if exit_code != 0:
        break

    data = logplotter.find_data("log.lammps")
    t = np.array(data["Time"]) * units.t0
    T = np.array(data["Temp"]) * units.T0
    num_frames = len(t)
    if k == 0:
        skip = num_frames // 200
        np.savetxt("data/Tfirst.dat",
                   np.array([t[::skip], T[::skip]]).transpose())
    for i in range(num_frames):
        if abs(T[i] - T[-1]) < 0.5 * abs(T[i] - T[0]):
            break
    equilibrium_frames = 3 * i
    assert equilibrium_frames < 0.8 * num_frames,\
        "Longer simulation time required to reach equilibrium."
    stddev[k] = np.std(T[equilibrium_frames:])
    k += 1

num_frames = len(t)
skip = num_frames // 200
np.savetxt("data/Tlast.dat", np.array([t[::skip], T[::skip]]).transpose())

sizes = sizes[:k]
stddev = stddev[:k]
np.savetxt("data/stddev.dat", np.array([sizes, stddev]).transpose())

np.savetxt("data/firstsize.dat", [sizes[0]], fmt="%d")
np.savetxt("data/lastsize.dat", [sizes[-1]], fmt="%d")

C, D = np.polyfit(np.log(sizes), np.log(stddev), deg=1)

np.savetxt("data/Lpower.dat", [C], fmt="%f")
