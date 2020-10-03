#!/bin/bash

sh ./bin/eastmoney_uwsgi.sh start
sh ./bin/nohup_run_nodejs_server.sh
sh ./bin/nohup_run_spider.sh
