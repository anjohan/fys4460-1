all: data/D.dat

data/D.dat: everything.py in.script ../units.py
	mkdir -p data
	python everything.py
data/log.msd_%: in.script
	lmp_mpi -var T $* -in in.script
