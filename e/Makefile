all:
	mkdir -p data
	python simulate.py
data/log.%: run.py in.script
	@python run.py $*
