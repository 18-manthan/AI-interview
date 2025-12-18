#!/bin/bash
set -e

# Apply database migrations
python manage.py migrate

# Start the development server with auto-reload
python manage.py runserver 0.0.0.0:8000
