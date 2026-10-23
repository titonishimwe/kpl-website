#!/usr/bin/env bash
# Render build: install dependencies, collect static files, migrate, seed admin.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_default_admin
