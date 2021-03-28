#!/bin/bash

set -e

echo "${0}: running migrations."
python manage.py migrate --noinput

echo "${0}: collecting statics."

python manage.py collectstatic --noinput
#python init_database.py
#python manage.py runserver 0.0.0.0:8000
python run_spider.py
