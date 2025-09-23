#!/usr/bin/env bash
set -o errexit

# Install dependencies 
pip install pipenv
pipenv install --deploy --system

# Apply database migrations
python manage.py migrate

# Create superuser when specified
if [ "$RUN_SUPERUSER_CREATION" = "True" ]; then
    echo "Creating Django superuser using environment variables..."

    python manage.py createsuperuser --noinput || true
    
    echo "Superuser creation command executed."
fi

