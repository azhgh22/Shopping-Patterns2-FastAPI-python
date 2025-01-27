help:
	echo "No Help"

install:
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry
	poetry install --no-root

lock:
	poetry lock --no-update

update:
	poetry update

format:
	poetry run ruff format playground tests
	poetry run ruff check  playground tests --fix

lint:
	poetry run ruff check playground tests
	poetry run mypy playground tests
