from multiprocessing.dummy import Pool as ThreadPool
import requests
from datetime import datetime


def crawl(url):
    response = requests.get(url)
    print("url {} status_code {} ".format(url, response.status_code))


start_time = datetime.now()
urls = [
    'http://www.python.org',
    'http://www.python.org/about/',
    'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
    'http://www.python.org/doc/',
    'http://www.python.org/download/',
    'http://www.python.org/getit/',
    'http://www.python.org/community/',
    'https://wiki.python.org/moin/',
]

for url in urls:
    crawl(url)

end_time = datetime.now()
print("cost: ", end_time - start_time)
