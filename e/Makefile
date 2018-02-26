data/plot.plt: plot.gpi data/relative_error.dat
	gnuplot plot.gpi
data/relative_error.dat: ../units.py analyse.py simulate.py
	mkdir -p data
	python simulate.py
	python analyse.py
	gnuplot plot.gpi
data/log.%: run.py in.script
	@python run.py $*
fig.pdf: fig.asy data/relative_error.dat
	asy fig.asy
