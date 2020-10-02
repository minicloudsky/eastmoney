#!/usr/bin/env bash

PROJECT_PATH=/home/.jywcode/eastmoneyspider
# shellcheck disable=SC2164
cd $PROJECT_PATH
source venv/bin/activate
pip3 install -r requirements.txt

python3 $PROJECT_PATH/manage.py makemigrations
python3 $PROJECT_PATH/manage.py migrate
python3 $PROJECT_PATH/manage.py collectstatic
