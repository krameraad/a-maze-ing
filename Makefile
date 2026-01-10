NAME = a_maze_ing.py
CONFIG = config.txt

# Commands --------------------------------------------------------------------

install:

run:
	python3 $(NAME) $(CONFIG)

debug:

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

# Phonies ---------------------------------------------------------------------

.PHONY: install run debug clean lint lint-strict
