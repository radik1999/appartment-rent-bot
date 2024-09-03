#!/bin/bash

# Django setup
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py create_default_superuser

# Run the application
exec "$@"
