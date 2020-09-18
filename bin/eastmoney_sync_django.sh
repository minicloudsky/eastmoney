#!/usr/bin/env bash

PROJECT_PATH=/home/.jywcode/EastMoneySpider
# shellcheck disable=SC2164
cd PROJECT_PATH
source venv/bin/activate
pip install -r requirements.txt

python $PROJECT_PATH/back_end/manage.py makemigrations
python $PROJECT_PATH/back_end/manage.py migrate
python $PROJECT_PATH/back_end/manage.py collectstatic
