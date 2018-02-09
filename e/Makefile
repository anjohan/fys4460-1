all:
	mkdir -p data
	python simulate.py
	python analyse.py
data/log.%: run.py in.script
	@python run.py $*
