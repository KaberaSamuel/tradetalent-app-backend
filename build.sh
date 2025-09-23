#!/usr/bin/env bash
set -o errexit

pip install pipenv
pipenv install --deploy --system

python manage.py migrate

mkdir -p /opt/render/project/src/staticfiles

python manage.py collectstatic --noinput --verbosity=2  # Added verbosity for debugging

# Uncomment to see what was collected:
echo "=== Static files collected ==="
ls -la /opt/render/project/src/staticfiles/ || echo "Directory not found"

if [ "$RUN_SUPERUSER_CREATION" = "True" ]; then
    python manage.py createsuperuser --noinput || true
fi