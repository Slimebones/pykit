set shell := ["nu", "-c"]

test target="" show="all" *flags="":
	poetry run coverage run -m pytest -x --ignore=tests/app -p no:warnings --show-capture={{show}} --failed-first {{flags}} {{target}}

lint target=".":
	poetry run ruff {{target}}

check: lint test

release version: check
	git add .
	git commit -m {{version}}
	git tag {{version}}
	git push
	git push --tags
