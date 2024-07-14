#!/bin/bash
echo "migrating database"
python manage.py migrate

# password comes from environment variable DJANGO_SUPERUSER_PASSWORD
echo "creating the superuser"
python manage.py createsuperuser --noinput --username admin --email admin@example.com

python manage.py runserver 0.0.0.0:8000