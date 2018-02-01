all:
	$(MAKE) -C a data/velocity_correlation.dat
	$(MAKE) report.pdf

report.pdf: report.tex a/data/velocity_correlation.dat
	rubber -v --pdf report.tex
