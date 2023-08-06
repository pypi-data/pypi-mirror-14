PYTHON=../venv/bin/python
MKDOCS=../venv/bin/mkdocs

.PHONY: build clean default

build:
	${MKDOCS} build --clean

serve:
	${MKDOCS} serve

clean:
	rm -rf site

default: build
	:
