all:
	$(MAKE) -C a data/velocity_correlation.dat
	$(MAKE) -C b data/stddev.dat
	$(MAKE) -C c data/stddev.dat
	$(MAKE) -C c data/P.dat
	$(MAKE) report.pdf

report.pdf: report.tex a/data/velocity_correlation.dat b/data/stddev.dat c/data/stddev.dat
	rubber -v --pdf report.tex
