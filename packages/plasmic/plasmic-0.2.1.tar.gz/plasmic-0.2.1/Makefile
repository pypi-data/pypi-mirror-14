# Copyright (C) 2016 The Meme Factory, Inc.  http://www.meme.com/

# This file is part of Plasmic.
#
# Plasmic is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Plasmic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Plasmic.  If not, see <http://www.gnu.org/licenses/>.

# Karl O. Pinc <kop@meme.com>

TARGETS =
EXTRA_TARGETS = README.html
SETUPTOOLS_STUFF = build dist plasmic.egg-info

all: ${TARGETS}

help:
	@echo
	@echo 'Usage: make TARGET'
	@echo
	@echo 'TARGET is one of:'
	@echo 'README.html         Make html version of README.rst'
	@echo 'publish             Update all public-facing info'
	@echo '                    ("check-manifest" + "upload" + "push")'
	@echo 'check-manifest      Run check-manifest'
	@echo 'update_check-manifest'
	@echo '                    Upgrade check-manifest venv to latest'
	@echo '                    versions'
	@echo 'clean               Removed generated data'
	@echo
	@echo 'Less used TARGETS are:'
	@echo 'register_test       Register project at pypi test site'
	@echo 'register            Register project at pypi live site'
	@echo 'upload_test         Upload project to pypi test site'
	@echo 'upload              Upload project to pypi live site'
	@echo 'push                Push repo changes to public repo'
	@echo '                    (Hooks at bitbucket update readthedocs)'
	@echo 'devel/check-manifest'
	@echo '                    Create a check-manifest venv'
	@echo
	@echo 'This Makefile does not work with the docs.  See:'
	@echo 'cd docs; make help'

README.html: README.rst
	rst2html --strict README.rst > README.html


# Useless targets
# Register with pypi.
.PHONY: register_test
register_test:
	python setup.py register -r https://testpypi.python.org/pypi

.PHONY: register
register:
	python setup.py register


# Not so useless targets, used by the package owners for package management
.PHONY: upload_test
upload_test:
	python setup.py sdist upload -r https://testpypi.python.org/pypi

.PHONY: upload
upload:
	python setup.py sdist upload

.PHONY: push
	hg push

.PHONY: publish
publish: check-manifest upload push


# Development related targets
devel:
	[ -d devel ] || mkdir devel

devel/check-manifest: devel
	[ -d devel/check-manifest ] \
	  || ( virtualenv devel/check-manifest ; \
	       devel/check-manifest/bin/pip install check-manifest )

update_check-manifest: devel/check-manifest
	devel/check-manifest/bin/pip -U

check-manifest: devel/check-manifest
	devel/check-manifest/bin/check-manifest


# Expected targets
.PHONY: clean
clean:
	$(MAKE) -C docs clean
	rm -rf ${TARGETS} ${EXTRA_TARGETS} ${SETUPTOOLS_STUFF} devel
