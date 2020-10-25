#!/usr/bin/env bash

PROJECT_PATH=/home/.jywcode/eastmoney/backend/crawler_nodejs
# shellcheck disable=SC2164
cd $PROJECT_PATH
npm install

nohup node  $PROJECT_PATH/index.js  > nohup.out & 
