#!/usr/bin/env bash

PROJECT_PATH=/home/.jywcode/EastMoneySpider
DESC=eastmoney_django_server
NAME=eastmoney_django_server
PIDFILE=$PROJECT_PATH/uwsgi/uwsgi.pid
STATUS_FILE=$PROJECT_PATH/uwsgi/uwsgi.status
DAEMONIZE_FILE=$PROJECT_PATH/uwsgi/$NAME.log
# shellcheck disable=SC2164
cd $PROJECT_PATH
source venv/bin/activate
pip install -r requirements.txt

server_start() {
  uwsgi --ini $PROJECT_PATH/uwsgi/eastmoney_uwsgi.ini --stats=$STATUS_FILE --pidfile=$PIDFILE --daemonize=$DAEMONIZE_FILE
}

server_stop() {
  uwsgi --stop $PIDFILE
}

server_status() {
  uwsgi --connect-and-read $STATUS_FILE
  return $?
}

case "$1" in
start)
  echo -n "Starting $DESC: "
  if [ -e $PIDFILE ]; then
    echo "The program has been started! Please check it!"
  else
    server_start
    sleep 5
    if [ -e $PIDFILE ]; then
      echo "Ok"
    else
      echo "Failed"
    fi
  fi
  ;;
stop)
  echo -n "Stopping $DESC: "
  if [ ! -e $PIDFILE ]; then
    echo "The program doesn't start!"
  else
    server_stop
    sleep 5
    if [ ! -e $PIDFILE ]; then
      echo "ok"
    fi
  fi
  ;;
restart | force-reload)
  echo -n "Restarting $DESC: "
  server_stop
  sleep 5
  if [ -e $PIDFILE ]; then
    echo "stop failed!"

  else
    echo "stop ok!"
  fi

  server_start
  sleep 5
  if [ -e $PIDFILE ]; then
    echo "start ok!"

  else
    echo "start Failed!"
  fi
  ;;
status)
  echo -n "Status of $DESC: "
  server_status && echo "running" || echo "stopped"
  ;;
*)
  N=/etc/init.d/$NAME
  echo "Usage: $N {start|stop|restart|status}" >&2
  exit 1
  ;;
esac

exit 0
