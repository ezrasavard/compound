init:
	pip3 install -r requirements.txt

test:
	nosetests tests

style:
	pep8 --first --show-source *.py
