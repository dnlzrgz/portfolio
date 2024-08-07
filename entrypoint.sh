#!/bin/bash

set -e

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Creating database cache table just in case..."
python manage.py createcachetable

# Collect static files and compress CSS files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create an admin user if it does not exist
echo "Creating admin user..."
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_ADMIN_USERNAME')
password = os.environ.get('DJANGO_ADMIN_PASSWORD')
email = os.environ.get('DJANGO_ADMIN_EMAIL')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f"Admin user {username} created.")
else:
    print(f"Admin user {username} already exists.")
EOF

# Start Django
WORKERS=${WORKERS:-17}
THREADS=${THREADS:-2}
MAX_REQUESTS=${MAX_REQUESTS:-1000}
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-50}
TIMEOUT=${TIMEOUT:-10}
gunicorn portfolio.wsgi:application --bind 0.0.0.0:${PORT} --workers ${WORKERS} --threads ${THREADS} --max-requests ${MAX_REQUESTS} --max-requests-jitter ${MAX_REQUESTS_JITTER} --timeout ${TIMEOUT} --preload --log-file "-"
