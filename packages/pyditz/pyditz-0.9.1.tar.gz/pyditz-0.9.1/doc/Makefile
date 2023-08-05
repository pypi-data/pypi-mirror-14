# Makefile for building interactive pyditz tutorial output.

PYTHON = python

SRCS = guide/start.rst guide/create.rst guide/query.rst guide/assign.rst \
guide/issues.rst guide/release.rst guide/export.rst guide/other.rst	 \
guide/vcs.rst guide/config.rst

RUNSESSION = $(PYTHON) -m ditz.session
CLEANFILES = .ditz-*

all: doc

doc:; cd .. && $(MAKE) doc

update: $(SRCS)
	@ $(MAKE) -s clean
	$(RUNSESSION) $(SRCS)

clean:
	rm -rf $(CLEANFILES)
