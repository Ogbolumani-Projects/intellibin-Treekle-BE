#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -o errexit  

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# (Optional) Run database migrations (Django)
if [ -f "manage.py" ]; then
    python manage.py migrate
fi