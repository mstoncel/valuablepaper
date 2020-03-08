#!/usr/bin/env bash

echo "Changes are being investigated on models."
python manage.py makemigrations

echo "Created migration files are running."
python manage.py migrate

echo "Starting Django project"

python manage.py runserver 0.0.0.0:8000

