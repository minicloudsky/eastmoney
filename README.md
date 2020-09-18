# EastMoneySpider

东方财富、天天基金股票基金证券数据爬虫

### Usage:

`git clone https://github.com/minicloudsky/EastMoneySpider.git`

### 创建虚拟环境

```bash
virtualenv venv
source venv/bin/activate
```

### 修改数据库,改为你自己的数据库

````bash
vim eastmoneyspider/settings.py
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

### 执行爬取基金

```bash
python run_spider.py
```
