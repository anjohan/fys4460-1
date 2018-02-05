import os
import sys

arg = sys.argv[1]
rho, T = arg.split("_")

cmd = "mpirun lmp_mpi -var rho %s -var T %s -in in.script > /dev/null" % (rho,
                                                                          T)
print(cmd)
os.system(cmd)
