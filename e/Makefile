all:
	./simulate.sh
data/log.%: run.py in.script
	mkdir -p data
	python run.py $*
