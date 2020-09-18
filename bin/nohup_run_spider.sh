#!/usr/bin/env bash

PROJECT_PATH=/home/.jywcode/EastMoneySpider
# shellcheck disable=SC2164
cd $PROJECT_PATH
source venv/bin/activate
pip install -r requirements.txt

nohup python $PROJECT_PATH/run_spider.py >> nohup.out & 
