#!/usr/bin/env bash
set -o errexit

pip install pipenv
pipenv install --deploy --system

python manage.py migrate