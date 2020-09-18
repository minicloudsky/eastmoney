import datetime

import requests

import execjs
# 东方财富基金


class EastMoneyFund:
    def __init__(self):
        self.get_fund()

    def get_fund(self):
        headers = {
            'Host': 'fund.eastmoney.com',
            'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        }
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        # 因为基金收益大部分晚上更新，这里爬取前一天的已经更新的收益
        day = str(datetime.datetime.now().day - 1)
        yesterday = "{}-{}-{}".format(year, month, day)
        fundrank_url = 'http://fund.eastmoney.com/data/rankhandler.aspx?' \
                       'op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd' \
                       '={}&ed={}&qdii=&tabSubtype=,,,,,' \
                       '&pi=1&pn=50000&dx=1&v=0.8119929489462407 '.format(yesterday, yesterday)
        print(fundrank_url)
        response = requests.get(fundrank_url, headers=headers)
        print(response.text)

    def to_int(self, val):
        try:
            if val:
                val = val.replace('%', '').replace('---', '')
                val = int(val)
                return val
            return -9999
        except Exception as e:
            val = -9999
        return val

    def to_float(self, val):
        try:
            if val:
                val = val.replace('%', '').replace('---', '')
                val = float(val)
                return val
            return -9999
        except Exception as e:
            val = -9999
        return val


if __name__ == '__main__':
    easymoney = EastMoneyFund()
