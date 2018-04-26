.PHONY: all help clean


SRC=sieve.py

all:
	python2.7 $(SRC)

help:
	@printf 'To run tests on every update, use:\n'
	@printf '\n'
	@printf '    when-changed $(SRC) -c make\n'
	@printf '\n'


clean:
	rm -fr __pycache__/
	rm -fr .pytest_cache/



