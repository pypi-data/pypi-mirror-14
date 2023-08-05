VIRTUALENV_DIR=venv
MKDOCS=$(VIRTUALENV_DIR)/bin/mkdocs

.PHONY: help virtual serve build clean

default: virtual build

help:
	@echo "Targets: virtual serve build clean"
	@echo ""
	@echo "virtual:  Build a python virtual enviroment and install mkdocs into it"
	@echo "          for use by other targets"
	@echo "serve:    Spin up a small webserver locally for viewing the site as is"
	@echo "build:    Compile the site into a static form for uploading"
	@echo "clean:    Remove any temporary files"

virtual: venv
	./venv/bin/pip install mkdocs

venv:
	virtualenv $(VIRTUALENV_DIR)

serve: site
	$(MKDOCS) serve

build: docs
	$(MKDOCS) build

clean:
	$(MKDOCS) build --clean
	rm -rf $(VIRTUALENV_DIR)
