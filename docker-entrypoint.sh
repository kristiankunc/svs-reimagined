#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate --noinput

# Start the Django application
exec "$@"
