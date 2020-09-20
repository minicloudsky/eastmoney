#!/bin/bash
PATH = pwd
cd $PATH

sh eastmoney_uwsgi.sh start
sh nohup_run_nodejs_server.sh
sh nohup_run_spider.sh
