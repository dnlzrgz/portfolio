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

dev-start:
	docker compose --profile dev up --build

dev-stop:
	docker compose --profile dev down

dev-logs:
	docker compose --profile dev logs -f

prod-start:
	docker compose --profile prod up -d --build

prod-stop:
	docker compose --profile prod down

prod-logs:
	docker compose --profile prod logs -f

dev:
	@make dev-stop
	@make dev-start
	@make dev-logs

prod:
	@make prod-stop
	@make prod-start
	@make prod-logs
