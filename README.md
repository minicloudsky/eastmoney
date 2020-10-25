# EastMoneySpider

东方财富、天天基金股票基金证券数据爬虫、数据分析可视化
### first of all, 本项目不构成任何投资建议，仅做技术学习用途,投资有风险，入市需谨慎！！！
### 如有侵权请联系我删除

### Usage:

`git clone https://github.com/minicloudsky/EastMoney.git`

### 创建 python3 虚拟环境
```bash
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

### 修改数据库,改为你自己的数据库


`vim backend/eastmoney/settings.py`

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
### 修改基金历史净值的爬取模式，因为历史数据经测试有一千多万条，因此为了提高爬取速度，可以第一次爬取全量数据，以后每天爬取增量数据，这样可以加快爬取速度


`vim backend/config.ini`

```bash
[CRAWL_MODE]
; 全量爬取，默认为全量爬取
crawl_mode = "ALL"
; 增量爬取
;crawl_mode = "APPEND"
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

### 启动服务,执行爬取基金,因为爬虫耗时较长,因此通过 `nohup` 放后台执行，具体可以查看 `backend/bin` 下面脚本
```bash
cd backend
sh bin/start_server.sh

```
### 数据可视化
- 简单的数据可视化可以用 [metabase](https://www.metabase.com/docs/latest/getting-started.html),根据需要自己写 `sql`或者设置过滤聚合条件就好了
- `metabase` docker 部署
- 登录服务器，执行 `docker run -d  -it -p 3000:3000 --name metabase metabase/metabase`.这里我们把metabase部署在 3000端口
- 打开 your_host:3000,设置下数据库连接，然后写 sql 就可以做数据可视化了，以下是我自己做的简单 demo

![](https://github.com/minicloudsky/EastMoneySpider/blob/master/img/1.png)
![](https://github.com/minicloudsky/EastMoneySpider/blob/master/img/2.png)
![](https://github.com/minicloudsky/EastMoneySpider/blob/master/img/3.png)
### metabase 官方文档 [metabase](https://www.metabase.com/docs/latest/getting-started.html)
