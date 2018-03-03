all:
	$(MAKE) -C a data/velocity_correlation.dat
	$(MAKE) -C b data/stddev.dat
	$(MAKE) -C c data/stddev.dat
	$(MAKE) -C d data/P.dat
	$(MAKE) -C e data/relative_error.dat
	$(MAKE) -C e data/plot.plt
	$(MAKE) -C e fig.pdf
	$(MAKE) -C f data/D.dat
	$(MAKE) -C g data/fccrdf.dat
	$(MAKE) -C i data/T_berendsen.dat
	$(MAKE) -C i data/T_nosehoover.dat
	$(MAKE) report.pdf

report.pdf: report.tex a/data/velocity_correlation.dat b/data/stddev.dat c/data/stddev.dat d/data/P.dat e/data/relative_error.dat Makefile e/data/plot.plt f/data/D.dat e/fig.pdf g/data/fccrdf.dat i/data/T_berendsen.dat i/data/T_nosehoover.dat
	latexmk -pdflua -shell-escape

clean:
	latexmk -c
	rm -rf __pycache__ pythontex-files-report *.pytxcode *.auxlock report.pdf *.run.xml
