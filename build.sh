#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

python manage.py spectacular --color --file schema.yml
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('surxez19@gmail.com', '#Password123')"
#python manage.py createsuperuser --no-input --email "something@gmail.com"
