#!/bin/bash

docker ps | grep eastmoney | awk '{print $1}' | xargs docker stop
docker ps -a | grep eastmoney | awk '{print $1}' | xargs docker rm
docker images | grep eastmoney | awk '{print $1}' | xargs docker rmi
