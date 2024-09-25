#!/bin/bash

# Django setup
python src/manage.py makemigrations
python src/manage.py migrate
python src/manage.py create_default_superuser

# load dummy data
python src/manage.py loaddata src/appartment/fixtures/appartments

# start telegram bot
python src/manage.py startbot

# Run the application
exec "$@"
