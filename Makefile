# Delete all compiled Python files
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✨ Clean up complete!"

# Format
format:
	@echo "🔍 Formatting..."
	ruff check . --fix
	djhtml .
	@echo "✨ Format complete!"

# Run linters using pre-commit
lint:
	@echo "🔍 Linting..."
	pre-commit run --all-files
	@echo "✨ Linting complete!"

# Check using Django's system-check
check:
	@echo "🔍 Running system checks..."
	python manage.py check
	python manage.py check --deploy
	python manage.py check --tag security
	@echo "✨ All checks done!"

# Update dependencies and pre-commit
update:
	@echo "🔄 Updating dependencies and pre-commit..."
	poetry update
	pre-commit autoupdate
	@echo "✨ Update complete!"

# Run tests
test:
	@echo "🧪 Running all tests..."
	python manage.py test
	@echo "✨ All tests complete!"

# Download highlight.js scripts and styles
download-highlight:
	@echo "📥 Downloading highlight.js scripts and css styles..."
	@mkdir -p static/styles static/js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/styles/github-dark.min.css -o static/css/highlight.css
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/highlight.min.js -o static/js/highlight.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/python.min.js -o static/js/python.highlight.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/css.min.js -o static/js/css.highlight.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/bash.min.js -o static/js/bash.highlight.js
	curl -sL https://unpkg.com/@highlightjs/cdn-assets@11.9.0/languages/django.min.js -o static/js/django.highlight.js
	@echo "✨ highlight.js scripts and styles downloaded and saved!"

# Collect static files
collect:
	@echo "📦 Collecting static files..."
	python manage.py collectstatic
	@echo "✨ Static files collected!"

# Start development Docker compose
dev-start:
	@echo "🚀 Starting development Docker compose..."
	docker compose --profile development up
	@echo "✨ Development Docker compose started!"

# Stop development Docker compose
dev-stop:
	@echo "🛑 Stopping development Docker compose..."
	docker compose --profile development down
	@echo "✨ Local Docker compose stopped!"

# Watch development Docker compose logs
dev-logs:
	@echo "👀 Watching containers logs..."
	docker compose --profile development logs -f
	@echo "✨ Watching containers logs finished!"

# Start production Docker compose
prod-start:
	@echo "🚀 Starting production Docker compose..."
	docker compose --profile production up -d --build
	@echo "✨ Production Docker compose started!"

# Stop production Docker compose
prod-stop:
	@echo "🛑 Stopping production Docker compose..."
	docker compose --profile production down
	@echo "✨ Production Docker compose stopped!"

# Watch production Docker compose logs
prod-logs:
	@echo "👀 Watching containers logs..."
	docker compose --profile production logs -f
	@echo "✨ Watching containers logs finished!"

# Setup project
setup:
	@make download-highlight
	poetry install
	pre-commit install
	pre-commit run --all-files
	@echo "✨ Project setup complete!"

# Start development environment
dev:
	@make dev-stop
	@make dev-start
	@make dev-logs

# Start production environment
prod:
	@make prod-stop
	@make prod-start
	@make prod-logs
