import numpy as np
#from units import units
from mpi4py import MPI
from lammps import PyLammps

comm = MPI.COMM_WORLD
myrank = comm.Get_rank()
num_procs = comm.Get_size()
print("Hello from %d out of %d processors" % (myrank, num_procs))

T = 50
dt = 0.005
num_steps = int(round(T / dt))

lmp = PyLammps()
lmp.file("in.script")
lmp.command("timestep %g" % dt)
lmp.run(num_steps)
print(num_steps)

data = lmp.runs[0].thermo
t = data.Time
energy = data.TotEng
num_frames = len(t)
for i in range(num_frames):
    if abs(energy[i] - energy[-1]) < 0.5 * (energy[0] - energy[-1]):
        break
equilibrium_steps = 4 * i

print(1)
comm.barrier()
print(2)

equilibrium_steps = comm.bcast(equilibrium_steps, root=0)
if equilibrium_steps >= num_steps / 2:
    print("More steps needed!")
    lmp.run(2 * equilibrium_steps - num_steps)
    if myrank == 0:
        data2 = lmp.runs[1].thermo
        t += data.Time
        energy += data.TotEng

if myrank == 0:
    t = np.array(t) * units.t0
    energy = np.array(energy) * units.E0
    stdddev = np.std(energy[equilibrium_steps:])
