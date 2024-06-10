.NOTPARALLEL: ;          # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell
.PHONY: all 			 			 # All targets are accessible for user
.DEFAULT: help 			 		 # Running Make will run the help target

PY = @.venv/bin/python
PYTHON = $(PY) -m
APP = limelight

# -------------------------------------------------------------------------------------------------
# help: @ List available tasks on this project
# -------------------------------------------------------------------------------------------------
help:
	@grep -oE '^#.[a-zA-Z0-9]+:.*?@ .*$$' $(MAKEFILE_LIST) | tr -d '#' |\
	awk 'BEGIN {FS = ":.*?@ "}; {printf "  make%-10s%s\n", $$1, $$2}'
	 
# -------------------------------------------------------------------------------------------------
#  all: @ Apply all checks at once
# -------------------------------------------------------------------------------------------------
all: format lint test

# -------------------------------------------------------------------------------------------------
# init: @ Setup local environment
# -------------------------------------------------------------------------------------------------
init: activate 
	@if [ ! -f requirements.txt ]; then $(MAKE) compile; fi
	$(MAKE) install

# -------------------------------------------------------------------------------------------------
# update: @ Update package dependencies and install them
# -------------------------------------------------------------------------------------------------
update: compile install

# -------------------------------------------------------------------------------------------------
# Activate virtual environment
# -------------------------------------------------------------------------------------------------
activate:
	@python3 -m venv .venv
	@. .venv/bin/activate 
	$(PYTHON) pip install pip-tools

# -------------------------------------------------------------------------------------------------
#  compile: @ Compile requirements.in files to requirements.txt
# -------------------------------------------------------------------------------------------------
compile:
	$(PYTHON) piptools compile --upgrade requirements.in 
	$(PYTHON) piptools compile --upgrade requirements-dev.in

# -------------------------------------------------------------------------------------------------
# Install packages to current environment
# -------------------------------------------------------------------------------------------------
install:
	$(PYTHON) pip install --upgrade pip
	$(PYTHON) piptools sync requirements.txt requirements-dev.txt

# -------------------------------------------------------------------------------------------------
#  start: @ Start the application
#  -------------------------------------------------------------------------------------------------
start:
	$(PYTHON) uvicorn $(APP).main:app --reload

# -------------------------------------------------------------------------------------------------
# test: @ Run tests using pytest
# -------------------------------------------------------------------------------------------------
test:
	$(PYTHON) pytest tests --cov=$(APP)

# -------------------------------------------------------------------------------------------------
# lint: @ Checks the source code against coding standard rules and safety
# -------------------------------------------------------------------------------------------------
lint: lint.flake8 lint.safety lint.docs

# -------------------------------------------------------------------------------------------------
# format: @ Format source code and auto fix minor issues
# -------------------------------------------------------------------------------------------------
format:
	$(PYTHON) black --quiet --line-length=100 $(APP)
	$(PYTHON) isort $(APP)

# -------------------------------------------------------------------------------------------------
# flake8 
# -------------------------------------------------------------------------------------------------
lint.flake8: 
	$(PYTHON) flake8 --exclude=.venv,.eggs,*.egg,.git,migrations,__init__.py \
									 --filename=*.py,*.pyx \
									 --max-line-length=100 .

# -------------------------------------------------------------------------------------------------
# safety 
#
# Ignored error codes:
# 	70612 - Ninja2 template injection
# -------------------------------------------------------------------------------------------------
lint.safety: 
	$(PYTHON) safety check --full-report --ignore 67599 --ignore 70612

# -------------------------------------------------------------------------------------------------
# pydocstyle
#
# Ignored error codes:
#   D100	Missing docstring in public module
#   D101	Missing docstring in public class
#   D102	Missing docstring in public method
#   D103	Missing docstring in public function
#   D104	Missing docstring in public package
#   D105	Missing docstring in magic method
#   D106	Missing docstring in public nested class
#   D107	Missing docstring in __init__
# -------------------------------------------------------------------------------------------------
lint.docs: 
	$(PYTHON) pydocstyle --convention=numpy --add-ignore=D100,D101,D102,D103,D104,D105,D106,D107 .

# -------------------------------------------------------------------------------------------------
# clean: @ Remove artifacts and temp files
# -------------------------------------------------------------------------------------------------
clean:
	@rm -rf .venv/ dist/ build/ *.egg-info/ .pytest_cache/ .coverage coverage.xml
	@find . | grep -E "\(__pycache__|\.pyc|\.pyo\$\)" | xargs rm -rf
