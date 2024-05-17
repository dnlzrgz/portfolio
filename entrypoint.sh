#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT
