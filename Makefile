celery:
	celery -A src.core.celery worker -l info

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