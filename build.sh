#!/usr/bin/env bash
set -o errexit

pip install pipenv
pipenv install --deploy --system

python manage.py migrate

python manage.py collectstatic --noinput --verbosity=2  


if [ "$RUN_SUPERUSER_CREATION" = "True" ]; then
    python manage.py createsuperuser --noinput || true
fi