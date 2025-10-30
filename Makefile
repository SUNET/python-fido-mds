TOPDIR:=        $(abspath .)
SOURCE=         $(TOPDIR)/src
UV=             $(shell which uv)
PIPSYNC=        $(UV) pip sync

reformat:
	# sort imports and remove unused imports
	$(UV) run ruff check --select F401,I --fix
	# reformat
	$(UV) run ruff format

typecheck:
	MYPYPATH=$(SOURCE) $(UV) run mypy --ignore-missing-imports -p fido_mds

update_package_data:
	cd $(TOPDIR)/scripts && make update_package_data

test:
	$(UV) run pytest src

build:
	# Update version to current YYYY.MM format
	sed -i "s/^version = .*/version = \"$$(date -u +'%Y.%-m')\"/" pyproject.toml
	@echo "Updated version in pyproject.toml to: $$(date -u +'%Y.%-m')"
	$(UV) pip install build[virtualenv]
	$(UV) build

dev_sync_deps:
	@test $${VIRTUAL_ENV?virtual env not activated}
	$(PIPSYNC) test_requirements.txt
	$(UV) pip install -r test_requirements.txt
