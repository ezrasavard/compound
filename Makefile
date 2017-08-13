init:
	pip3 install -r requirements.txt

test:
	python3 -m nose tests

style:
	pep8 . --first --show-source
