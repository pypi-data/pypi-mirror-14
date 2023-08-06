all: test

VERSION = `cat version.txt | xargs`

IMAGE = fmap-dev
PYDEV = docker run --rm -it -e BE_UID=`id -u` -e BE_GID=`id -g` \
	-v $(CURDIR):/app $(IMAGE)
VERSIONS = 2.7.11,3.3.6,3.4.4,3.5.1

#-------------------------------------------------------------------------------
# Docker image management

docker-build:
	@docker build -t $(IMAGE):latest --build-arg versions=$(VERSIONS) .

docker-rmi:
	@docker rmi $(IMAGE)

docker-shell:
	@$(PYDEV) bash

.PHONY: docker-build docker-rmi docker-shell
#-------------------------------------------------------------------------------
# Build management

check:
	@$(PYDEV) check-manifest

build: check
	@$(PYDEV) python setup.py sdist bdist_wheel

.PHONY: check build
#-------------------------------------------------------------------------------
# Documentation

docs:
	@$(MAKE) -C docs html

view:
	@python -c "import webbrowser as wb; \
	wb.open('docs/_build/html/index.html')"

.PHONY: docs view
#-------------------------------------------------------------------------------
# Dependency management

pip-compile:
	@$(PYDEV) pip-compile dev-requirements.in
	@$(PYDEV) pip-compile requirements.in

.PHONY: pip-compile
#-------------------------------------------------------------------------------
# Tests

test:
	@$(PYDEV) coverage erase
	@$(PYDEV) tox
	@$(PYDEV) coverage html

dist-test: build
	@$(PYDEV) dist-test $(VERSION)

show:
	@python -c "import webbrowser as wb; wb.open('htmlcov/index.html')"

.PHONY: test show
#-------------------------------------------------------------------------------
# Cleanup

clean: 
	@rm -f *.py[co] */*.py[co] */*/*.py[co]
	@rm -rf */__pycache__ */*/__pycache__
	@$(MAKE) -C docs clean

.PHONY: clean
#-------------------------------------------------------------------------------
