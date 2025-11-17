MAIN = main
OUTNAME = main.pdf
OUTDIR = latex.out

LATEXRUN = latexrun.py
LATEXCMD = xelatex

all: build

build:
	-python3 $(LATEXRUN) -o $(OUTNAME) -O $(OUTDIR) --latex-cmd $(LATEXCMD) --bibtex-cmd biber $(MAIN).tex 2>&1 >/dev/null | true
	python3 $(LATEXRUN) -o $(OUTNAME) -O $(OUTDIR) --latex-cmd $(LATEXCMD) --bibtex-cmd biber $(MAIN).tex

preview:
	convert -density 80 $(OUTNAME).pdf $(OUTNAME)-thumb.png
	convert -density 250 $(OUTNAME).pdf $(OUTNAME).png

clean:
	python3 $(LATEXRUN) --clean-all
	rm -rf $(OUTDIR)
	rm -f $(OUTNAME) *.png
