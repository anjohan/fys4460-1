all: data/fccrdf.dat

data/fccrdf.dat: everything.py in.script ../units.py
	mkdir -p data
	ovitos everything.py
data/log.%: in.script
	@lmp_mpi -var T $* -in in.script > /dev/null
