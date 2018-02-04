import sys
from mpi4py import MPI
from lammps import lammps

myrank = MPI.COMM_WORLD.Get_rank()
num_procs = MPI.COMM_WORLD.Get_size()

print("Hello from %d out of %d processors" % (myrank, num_procs))

lmp = lammps()
lmp.file("in.script")

assert len(sys.argv) == 2, "Give dt as cmd line argument!"
dt = float(sys.argv[1])
lmp.command("run 0")
t = lmp.get_thermo("time")
print(t)
