data/velocity_correlation.dat: velocity_distribution.py data/simulation.in.bin ../units.py
	ovitos velocity_distribution.py
data/simulation.in.bin: in.simulation data/uniformvelocity.data
	mpirun lmp_mpi -in in.simulation
	mv log.lammps data/log.simulation
data/uniformvelocity.data: data/fcc.data generate_velocities.py
	python generate_velocities.py
data/fcc.data: in.generatefcc
	mkdir -p data
	mpirun lmp_mpi -in in.generatefcc
	mv log.lammps data/log.fcc
