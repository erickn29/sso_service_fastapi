ruff:
	ruff check . --fix

black:
	black .

mypy:
	mypy .

cool:
	ruff check . --fix
	black .
	mypy .