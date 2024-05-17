#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT
