lint:
	poetry run isort --check .
	poetry run black --check .
	poetry run flake8
	poetry run mypy --install-types --non-interactive -p app -p tests
