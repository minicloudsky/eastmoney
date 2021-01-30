#!/bin/bash
PROJECT_PATH=$(cd "$(dirname "$0")"; cd ../;pwd)
echo $PROJECT_PATH
sh $PROJECT_PATH/bin/eastmoney_uwsgi.sh start
sh $PROJECT_PATH/bin/nohup_run_nodejs_server.sh
sh $PROJECT_PATH/bin/nohup_run_spider.sh
sh $PROJECT_PATH/bin/nohup_run_django_server.sh
