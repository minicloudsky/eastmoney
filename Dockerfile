FROM python:3.6
ADD . /code
WORKDIR /code
RUN apt-get update -y
RUN apt-get install  zlib
RUN apt-get install  libjpeg
RUN apt-get install  libjpeg-devel
RUN apt-get install  zlib-devel
RUN pip install -r requirements.txt   --trusted-host mirrors.cloud.aliyuncs.com  -i http://mirrors.cloud.aliyuncs.com/pypi/simple/
CMD ["python","manage.py","makemigrations"]
CMD ["python","manage.py","migrate"]
CMD ["python", "manage.py","runserver"]
CMD ["python","run_spider.py"]
