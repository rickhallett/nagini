.PHONY: edit clean data s3/upload s3/download requirements

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = nagini

AWS_BUCKET = [OPTIONAL] your bucket and folder for s3, as you would use it with the aws cli. Do not include a trailing / in the url. For example s3://foo/bar
# use AWS_DEFAULT_PROFILE to change the profile used
PYTHONPATH = $(CURDIR)

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Run Jupyter Lab
edit: .make/requirements
	PYTHONPATH=$(PYTHONPATH) \
		poetry run jupyter lab --ip 0.0.0.0

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Make Dataset
data: .make/requirements
	PYTHONPATH=$(PYTHONPATH) \
		poetry run python -m src.data.make_dataset data/raw data/processed

## Upload Data to S3
s3/upload:
	aws s3 sync data/ $(AWS_BUCKET)/data/
	aws s3 sync models/ $(AWS_BUCKET)/models/

## Download Data from S3
s3/download:
	aws s3 sync $(AWS_BUCKET)/data/ data/
	aws s3 sync $(AWS_BUCKET)/models/ models/

## Install Python Dependencies
requirements: .make/requirements

.make/requirements: pyproject.toml
ifneq (,$(wildcard .python-version))
	poetry env use $(shell cat .python-version)
endif
	PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry install
	if [ ! -e .make ]; then mkdir .make; fi
	touch $@

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
.PHONY: show-help
show-help:
	@echo "$$(tput setaf 2)Available rules:$$(tput sgr0)";sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## /---/;td" -e"s/:.*//;G;s/\\n## /===/;s/\\n//g;p;}" ${MAKEFILE_LIST}|awk -F === -v n=$$(tput cols) -v i=4 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"- %s%s%s\n",a,$$1,z;m=split($$2,w,"---");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;}printf"%*s%s\n",-i," ",w[j];}}'
