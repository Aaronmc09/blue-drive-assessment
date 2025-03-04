#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
python manage.py wait_for_db

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py shell << END
from author.models import User
import os

admin_email = os.getenv('DJANGO_ADMIN_EMAIL', 'admin@django.com')
admin_password = os.getenv('DJANGO_ADMIN_PASSWORD')

if not admin_password:
    print('Error: DJANGO_ADMIN_PASSWORD environment variable is not set')
    exit(1)

if not User.objects.filter(email=admin_email).exists():
    User.objects.create_superuser(email=admin_email, password=admin_password)
    print('Superuser created successfully!')
else:
    print('Superuser already exists.')
END

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000 