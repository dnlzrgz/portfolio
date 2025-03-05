lint:
	uvx djlint ./templates --profile=jinja
	uvx djlint ./templates --profile=jinja --reformat

setup:
	curl -sLo tailwind https://github.com/tailwindlabs/tailwindcss/releases/download/v4.0.9/tailwindcss-linux-x64
	curl -sLo ./static/js/alpine.js https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js

tailwind:
	./tailwind -i ./static/css/input.css -o ./output/static/css/output.css --watch

serve:
	python3 -m http.server 8000 --directory ./output/

build:
	uv run marastatic.py --config-file config.toml
	./tailwind -i ./static/css/input.css -o ./output/static/css/output.css --minify

