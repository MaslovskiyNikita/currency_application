#!/bin/bash

python manage.py makemigrations
python manage.py migrate

python manage.py sync_currencies

python -m gunicorn src.config.wsgi:application --bind 0.0.0.0:8000 --workers 4 
