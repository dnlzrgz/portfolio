clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint:
	uvx ruff check . --fix
	uvx djhtml .

check:
	uv run python manage.py check
	uv run python manage.py check --deploy
	uv run python manage.py check --tag security

update:
	uv lock --upgrade
	uv sync

download-highlight:
	curl -sL https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css -o static/css/highlight.css
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/highlight.min.js -o static/js/highlight.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/css.min.js -o static/js/highlight.css.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/go.min.js -o static/js/highlight.go.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/html.min.js -o static/js/highlight.html.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/javascript.min.js -o static/js/highlight.javascript.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/python.min.js -o static/js/highlight.python.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/sql.min.js -o static/js/highlight.sql.js

collect:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

local:
	uv run python manage.py runserver

docker-start:
	docker compose up -d --build

docker-stop:
	docker compose down

docker-logs:
	docker compose logs -f

docker:
	@make docker-stop
	@make docker-start
	@make docker-logs
