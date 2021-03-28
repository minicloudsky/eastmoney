FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt   -i https://pypi.douban.com/simple/ --trusted-host https://pypi.douban.com/simple/
RUN pip install --upgrade mysqlclient -i https://pypi.douban.com/simple/ --trusted-host https://pypi.douban.com/simple/
COPY  base.py /usr/local/lib64/python3.6/site-packages/django/db/backends/mysql/base.py 
CMD ["python", "init_database.py"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0:8000"]
CMD ["python","run_spider.py"]
