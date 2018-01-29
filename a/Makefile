all: data/simulation.in.bin

data/simulation.in.bin: in.simulation data/uniformvelocity.data
	mpirun -n 4 lmp_mpi -in in.simulation
	mv log.lammps data/log.simulation
data/uniformvelocity.data: data/fcc.data generate_velocities.py
	python generate_velocities.py
data/fcc.data: in.generatefcc
	mkdir data
	mpirun -n 4 lmp_mpi -in in.generatefcc
	mv log.lammps data/log.fcc
