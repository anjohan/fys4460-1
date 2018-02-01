all:
	$(MAKE) -C a data/velocity_correlation.dat
	$(MAKE) report.pdf

report.pdf: report.tex
	rubber -v --pdf report.tex
