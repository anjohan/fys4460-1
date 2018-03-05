all: data/D.dat

data/D.dat: everything.py in.script ../units.py spce-water-system.in
	mkdir -p data
	ovitos everything.py
spce-water-system.in: spce-water-system.lt spce-simple.lt
	moltemplate.sh -atomstyle "full" spce-water-system.lt
data/log.%: in.script
	lmp_mpi -var T $* -in in.script
