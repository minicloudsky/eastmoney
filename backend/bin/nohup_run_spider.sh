#!/usr/bin/env bash

PROJECT_PATH=$(cd "$(dirname "$0")"; cd ../;pwd)
# shellcheck disable=SC2164
cd $PROJECT_PATH
source venv/bin/activate
pip3 install -r requirements.txt
docker start mysql
nohup python3 $PROJECT_PATH/run_spider.py > nohup.out & 
