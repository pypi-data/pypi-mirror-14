.PHONY: tests devinstall docs
APP=nasapi
COV=nasapi
OPTS=

tests:
	py.test -s -v $(APP)

devinstall:
	pip install -e .
	pip install -e .[tests]

docs:
	sphinx-apidoc --force -o docs/source/modules/ nasapi
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
