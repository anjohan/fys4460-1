data/plot.plt: plot.gpi
	gnuplot plot.gpi
data/relative_error.dat: ../units.py analyse.py simulate.py
	mkdir -p data
	python simulate.py
	python analyse.py
data/log.%: run.py in.script
	@python run.py $*
