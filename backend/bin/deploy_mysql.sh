# /us/bin/bash
# $MYSQL_ROOT_PASSWORD=root

echo "start deploy mysql"
mkdir -p /home/container/mysql/conf
mkdir -p /home/container/mysql/data
mkdir -p /home/container/mysql/log
mkdir -p /home/container/mysql/mysql-files
echo "mysql mount dir created ."
docker pull mysql
docker  run  -it --name  mysql -p 3306:3306   -e MYSQL_ROOT_PASSWORD=root   -v   /home/container/mysql/log/:/var/log/mysql  -v /home/container/mysql/conf/:/etc/mysql -v   /home/container/mysql/data:/var/lib/mysql    -v   /home/container/mysql/mysql-files/:/var/lib/mysql-files -d mysql
echo "mysql deploy completed ."
