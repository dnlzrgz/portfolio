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

# Download v1.9.12 of htmx and plugins
download-htmx:
	@echo "📥 Downloading htmx script..."
	curl -sL https://unpkg.com/htmx.org@1.9.12/dist/htmx.js -o static/js/htmx.js
	curl -sL https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js -o static/js/htmx.min.js
	curl -sL https://unpkg.com/htmx.org@1.9.12/dist/ext/head-support.js -o static/js/head-support.js
	@echo "✨ htmx script downloaded and saved!"

# Collect static files
collect:
	@echo "📦 Collecting static files..."
	python manage.py collectstatic
	@echo "✨ Static files collected!"

# Start development Docker compose
dev-start:
	@echo "🚀 Starting development Docker compose..."
	docker compose -f ./dev.yaml up -d --build
	@echo "✨ Development Docker compose started!"

# Stop development Docker compose
dev-stop:
	@echo "🛑 Stopping development Docker compose..."
	docker compose -f dev.yaml down
	@echo "✨ Local Docker compose stopped!"

# Watch development Docker compose logs
dev-logs:
	@echo "👀 Watching containers logs..."
	docker compose -f dev.yaml logs -f
	@echo "✨ Watching containers logs finished!"

# Remove and restart development Docker compose
dev-restart:
	@make dev-stop
	@make dev-start

# Start production Docker compose
prod-start:
	@echo "🚀 Starting production Docker compose..."
	docker compose -f ./prod.yaml up -d --build
	@echo "✨ Production Docker compose started!"

# Stop production Docker compose
prod-stop:
	@echo "🛑 Stopping production Docker compose..."
	docker compose -f prod.yaml down
	@echo "✨ Production Docker compose stopped!"

# Watch production Docker compose logs
prod-logs:
	@echo "👀 Watching containers logs..."
	docker compose -f prod.yaml logs -f
	@echo "✨ Watching containers logs finished!"

# Remove and restart production Docker compose
prod-restart:
	@make prod-stop
	@make prod-start

# Setup project
setup:
	@make download-htmx
	poetry install
	pre-commit install
	pre-commit run --all-files
	@echo "✨ Project setup complete!"

# Start development environment
dev:
	@make dev-restart
	@make dev-logs

# Start production environment
prod:
	@make prod-restart
	@make prod-logs
