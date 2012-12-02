SHELL = /bin/bash
PYTHON = python
WGET = wget

PYTHON_VERSION := $(shell $(PYTHON) -V 2>&1)
BOOTSTRAP_PY_URL = http://svn.zope.org/*checkout*/zc.buildout/branches/2/bootstrap/bootstrap.py

install: parts/freetds
	CFLAGS="-I$(PWD)/parts/freetds/include" LDFLAGS="-L$(PWD)/parts/freetds/lib" $(PYTHON) setup.py install

toxtest: bin/tox
	CFLAGS="-I$(PWD)/parts/freetds/include" LDFLAGS="-L$(PWD)/parts/freetds/lib" LD_LIBRARY_PATH="$(PWD)/parts/freetds/lib" bin/tox

bin/tox: bin/buildout buildout.cfg
	$(MAKE) do_buildout

parts/freetds: bin/buildout buildout.cfg
	$(MAKE) do_buildout

do_buildout:
	if [[ "$(PYTHON_VERSION)" == Python\ 3* ]]; then echo "*** Python 3 ***"; bin/buildout -c buildout-py3.cfg; else echo "*** Python 2 ***"; bin/buildout; fi

bin/buildout: bootstrap.py
	$(PYTHON) bootstrap.py

bootstrap.py:
	$(WGET) -O bootstrap.py $(BOOTSTRAP_PY_URL)

clean:
	$(RM) -r bin/python bin/cython bin/buildout bin/tox develop-eggs eggs parts var .installed.cfg
	$(PYTHON) setup.py clean
