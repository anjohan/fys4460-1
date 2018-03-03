all: data/T_nosehoover.dat data/T_berendsen.dat

data/T_%.dat: data/log.T_% ../logplotter.py
	python ../logplotter.py -f $< -x Time -y Temp --dump $@ --noshow
data/log.T_%: in.%
	lmp_mpi -in $< > /dev/null
