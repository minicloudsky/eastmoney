from multiprocessing.dummy import Pool as ThreadPool
import requests
from datetime import datetime
import os


def crawl(url):
    response = requests.get(url)
    print("thread {} url {} status_code {} ".format(os.getpid(), url, response.status_code))


start_time = datetime.now()
urls = [
    'http://www.baidu.com',
    'http://www.zhihu.com',
    'http://www.360.cn',
    'http://www.sougou.com',
    'http://www.huawei.com',
    'http://www.2345.com',
    'http://www.qq.com',
    'https://tencent.com',
]

# Make the Pool of workers
pool = ThreadPool(8)
# Open the URLs in their own threads
# and return the results
results = pool.map(crawl, urls)
# Close the pool and wait for the work to finish
pool.close()
pool.join()
end_time = datetime.now()
print("cost: ", end_time - start_time)
print(results)
