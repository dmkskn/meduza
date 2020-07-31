build:
	pipenv run python setup.py sdist bdist_wheel

publish:
	pipenv run twine upload dist/*

pre-commit:
	pipenv run pre-commit install

test:
	pipenv run python -m unittest discover -s tests/

format:
	pipenv run black meduza.py setup.py tests

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

ci:
	pipenv run black --check meduza.py setup.py tests/
	pipenv run python -m unittest discover -s tests/
