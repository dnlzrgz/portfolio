#!/bin/bash

set -e

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

if [ "${USE_DATABASE_AS_CACHE}" = "True" ]; then
	python manage.py createcachetable
fi

# Collect static files
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
gunicorn portfolio.wsgi:application --bind 0.0.0.0:$PORT --workers $WORKERS --threads $THREADS --log-file "-"
