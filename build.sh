#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.oy makemigrations
python manage.py migrate

python manage.py spectacular --color --file schema.yml
python manage.py createsuperuser date_of_birth=2020-01-01 --no-input 
