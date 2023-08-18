export PYTEST_SHOW=all
export t=.
export version

test:
	poetry run coverage run -m pytest -x --ignore=tests/app -p no:warnings --show-capture=$(PYTEST_SHOW) --failed-first $(t)

lint:
	poetry run ruff $(t)

check: lint test

coverage:
	poetry run coverage report -m

coverage.html:
	poetry run coverage html --show-contexts && python -m http.server -d htmlcov 8000

publish:
	rm -f .readme.md
	cp ../README.md .readme.md
	git add .
	git commit -m "$(version)"
	git tag $(version)
	poetry publish --build
	git push
	git push --tags
