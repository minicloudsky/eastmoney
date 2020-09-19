from datetime import datetime
import requests
from urllib.parse import urlencode


# 东方财富基金


class EastMoneyFund:
    nodejs_server_url = 'http://127.0.0.1:3000?type='
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    max_size = 999999999999
    max_fund_num = 100000
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        'Referer': "http://fund.eastmoney.com/data/diyfundranking.html",
        'Host': "fund.eastmoney.com",
    }

    def __init__(self):
        # self.parse_fund_ranking()
        self.parse_diy_fund_ranking()

    def parse_fund_ranking(self):
        url = self.nodejs_server_url + "fund_ranking"
        print(url)
        response = requests.get(url)
        print(response.json())

    def parse_diy_fund_ranking(self):
        url = self.nodejs_server_url + "diy_fund_ranking"
        print(url)
        response = requests.get(url)
        print(response.json())

    def get_history_net_worth(self, fund_code):
        data = []

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
