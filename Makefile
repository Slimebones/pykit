export t=.

docs.serve:
	poetry run mkdocs serve -a localhost:9000 -w $(t)

docs.build:
	poetry run mkdocs build
