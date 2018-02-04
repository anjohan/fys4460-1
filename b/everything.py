import os
import logplotter
import numpy as np
from units import units

T = 50
dts = 0.005 * np.arange(2, 101) * 0.1
num_dts = len(dts)
stddev = np.zeros(num_dts)
for k in range(num_dts):
    dt = dts[k]
    num_steps = int(round(T / dt))

    exit_code = os.system(
        "mpirun lmp_mpi -var dt %g -var num_steps %d -in in.script" %
        (dt, num_steps))
    if exit_code != 0:
        break

    data = logplotter.find_data("log.lammps")
    t = np.array(data["Time"]) * units.t0
    E = np.array(data["TotEng"]) * units.E0
    num_frames = len(t)
    if k == 0:
        skip = num_frames // 200
        np.savetxt("data/Efirst.dat",
                   np.array([t[::skip], E[::skip]]).transpose())
    """
    for i in range(num_frames):
        if abs(E[i] - E[-1]) < 0.5 * abs(E[i] - E[0]):
            break
    equilibrium_frames = i
    assert equilibrium_frames < 0.8 * num_frames,\
        "Longer simulation time required to reach equilibrium."
    """
    stddev[k] = np.nanstd(E[num_frames // 10:])
    k += 1

num_frames = len(t)
skip = num_frames // 200
np.savetxt("data/Elast.dat", np.array([t[::skip], E[::skip]]).transpose())

dts = dts[:k]
stddev = stddev[:k]
np.savetxt("data/stddev.dat", np.array([dts, stddev]).transpose())

np.savetxt("data/firstdt.dat", [dts[0]], fmt="%f")
np.savetxt("data/lastdt.dat", [dts[-1]], fmt="%f")
