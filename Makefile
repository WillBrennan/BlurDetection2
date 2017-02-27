install_deps:
	pip install -U -r requirements.txt

install:
	pip install ./

test:
	py.test

yapf:
	find . -type f -name "*.py" | xargs yapf -i
