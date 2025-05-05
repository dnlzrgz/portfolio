lint:
	uvx djlint ./templates --profile=jinja --reformat

setup:
	curl -sLo tailwind https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.4/tailwindcss-linux-x64
	curl -sLo ./static/css/leaflet.css https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
	curl -sLo ./static/js/alpine.js https://cdn.jsdelivr.net/npm/alpinejs@3.14.8/dist/cdn.min.js
	curl -sLo ./static/js/quicklink.js https://cdnjs.cloudflare.com/ajax/libs/quicklink/2.3.0/quicklink.umd.js
	curl -sLo ./static/js/leaflet.js https://unpkg.com/leaflet@1.9.4/dist/leaflet.js

serve:
	python3 -m http.server 8000 --directory ./output/

images:
	uv run images.py

dev:
	uv run marastatic.py -c config.dev.toml
	./tailwind -i ./static/css/input.css -o ./output/static/css/output.css --minify


build:
	uv run marastatic.py -c config.toml
	uv run images.py
	./tailwind -i ./static/css/input.css -o ./output/static/css/output.css --minify

deploy:
	rm -rf output && mkdir output
	make build
	npx wrangler pages deploy output --project-name dnlzrgz

