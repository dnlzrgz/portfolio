clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint:
	uvx ruff check . --fix
	uvx djhtml .

check:
	uv run manage.py check
	uv run manage.py check --deploy
	uv run manage.py check --tag security

update:
	uv lock --upgrade
	uv sync

download-p5js:
	curl -sL https://cdn.jsdelivr.net/npm/p5@1.11.1/lib/p5.min.js -o static/js/p5.min.js

collect:
	uv run manage.py collectstatic --no-input

migrate:
	uv run manage.py migrate

build:
	uv run manage.py build

buildserver:
	uv run manage.py buildserver

publish:
	npx wrangler pages deploy /tmp/build

runserver:
	uv run manage.py runserver
