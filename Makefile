build:
	pipenv run python setup.py sdist bdist_wheel

publish:
	pipenv run twine upload dist/*

pre-commit:
	pipenv run pre-commit install

test:
	pipenv run pytest --exitfirst tests/

mypy:
	pipenv run mypy meduza

format:
	pipenv run black meduza setup.py tests

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr .pytest_cache/
	rm -fr .mypy_cache/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

ci:
	pipenv run black --check meduza setup.py tests
	pipenv run mypy meduza
	pipenv run pytest --exitfirst tests/
