#!/usr/bin/env bash

PROJECT_PATH=$(cd "$(dirname "$0")"; cd ../;pwd)
# shellcheck disable=SC2164
cd $PROJECT_PATH/crawler_nodejs
npm install

nohup node  $PROJECT_PATH/crawler_nodejs/index.js  > nohup.out & 
