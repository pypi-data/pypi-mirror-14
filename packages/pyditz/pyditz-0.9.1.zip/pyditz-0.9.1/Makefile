# Makefile for PyDitz.

PYTHON = python$(VER)
SETUP  = $(PYTHON) setup.py
ISSUES = doc/issues
STATIC = build/sphinx/html/_static
SRCS   = ditz tests

CLEANFILES = build dist *.egg* *.zip

.DEFAULT:;	@ $(SETUP) $@
.PHONY:		build doc

all:		build

build:;		@ $(SETUP) $@

doc:		issues
		@ $(SETUP) $@

issues:;	@ touch doc/index.rst
		@ rm -rf $(ISSUES) $(STATIC)
		@ $(PYTHON) -m ditz export html $(ISSUES)

tags:;		find $(SRCS) -name '*.py' | xargs etags

clean:;		$(SETUP) $@
		rm -rf $(CLEANFILES)
