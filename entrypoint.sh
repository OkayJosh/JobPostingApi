#!/usr/bin/env bash

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate --noinput

# Seed database with username bent, password 5478
python manage.py create_user bent 5478
# test
pytest

# Start Gunicorn server
gunicorn -b :8000 job_board.wsgi