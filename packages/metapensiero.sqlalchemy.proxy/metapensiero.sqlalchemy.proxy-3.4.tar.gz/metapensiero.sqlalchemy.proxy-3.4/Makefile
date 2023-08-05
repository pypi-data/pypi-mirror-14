# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy
# :Created:   lun 23 dic 2013 01:04:37 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2013, 2014, 2015, 2016 Lele Gaifax
#

PYTHON := $(BINDIR)python
BUMPER := bump_version
VERSION_TXT := version.txt
VERSION = $(shell cat $(VERSION_TXT))

.PHONY: check
check:
	py.test src/

.PHONY: bump-minor-version
bump-minor-version:
	$(BUMPER) $(VERSION_TXT)

.PHONY: bump-major-version
bump-major-version:
	$(BUMPER) -f major $(VERSION_TXT)

.PHONY: assert-clean-tree
assert-clean-tree:
	@(test -z "$(shell git status -s --untracked=no)" || \
	  (echo "UNCOMMITTED STAFF" && false))

.PHONY: assert-master-branch
assert-master-branch:
	@(test "$(shell git rev-parse --abbrev-ref HEAD)" = "master" || \
	  (echo "NOT IN MASTER BRANCH" && false))

.PHONY: release
release: assert-master-branch assert-clean-tree
	$(MAKE) bump-minor-version
	@echo ">>>"
	@echo ">>> Do your duties (update CHANGES.rst for example), then"
	@echo ">>> execute “make tag-release”."
	@echo ">>>"

.PHONY: major-release
major-release: assert-master-branch assert-clean-tree
	$(MAKE) bump-major-version
	@echo ">>>"
	@echo ">>> Do your duties (update CHANGES.rst for example), then"
	@echo ">>> execute “make tag-release”."
	@echo ">>>"

.PHONY: tag-release
tag-release: assert-master-branch check-release-date check-long-description-markup
	git commit -a -m "Release $(VERSION)"
	git tag -a -m "Version $(VERSION)" v$(VERSION)

.PHONY: check-long-description-markup
check-long-description-markup:
	@$(PYTHON) setup.py check -r -s

.PHONY: check-release-date
check-release-date:
	@fgrep -q "$(VERSION) ($(shell date --iso-8601))" CHANGES.rst \
	  || (echo "ERROR: release date of version $(VERSION) not set in CHANGES.rst"; exit 1)

.PHONY: pypi-upload
pypi-upload: assert-master-branch assert-clean-tree
	$(PYTHON) setup.py sdist upload

.PHONY: publish
publish: pypi-upload
	git push
	git push --tags
