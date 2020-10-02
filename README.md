# EastMoneySpider

东方财富、天天基金股票基金证券数据爬虫

### Usage:

`git clone https://github.com/minicloudsky/EastMoneySpider.git`

### 创建 python3 虚拟环境

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

### 修改数据库,改为你自己的数据库


`vim eastmoneyspider/settings.py`

```python
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'your database host',
        'PORT': 3306,
        'USER': 'your database user',
        'PASSWORD': 'your database password',
        'NAME': 'your database name'
    }
}
````

### 安装依赖包

```bash
pip install -r requirements.txt
```
### 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```
### admin 静态文件 迁移
```bash
python3 manage.py collectstatic
```
### 启动服务
```bash

sh bin/start_server.sh

```
### 执行爬取基金,因为爬虫耗时较长，建议 `nohup` 放后台执行

```bash
nohup python run_spider.py > nohup.out & 
```
