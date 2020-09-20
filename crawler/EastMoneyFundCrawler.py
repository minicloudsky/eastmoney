import json
from datetime import datetime
import requests
from urllib.parse import urlencode
import logging
from apps.Fund.models import FundHistoricalNetWorthRanking, FundLog, Fund

logger = logging.getLogger("easymoneyfundcrawler")


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
        logger.warning("{} start parsing fund ranking".format(datetime.now()))
        url = self.nodejs_server_url + "fund_ranking"
        log_kwargs = {}
        log_kwargs['name'] = '爬取基金排行'
        log_kwargs['start_time'] = datetime.now()
        response = requests.get(url)
        funds_json = response.json()
        if funds_json:
            all_fund = funds_json['datas']
            fund_historical_networth_ranking_object_list = []
            fund_object_list = []
            for fund in all_fund:
                kwargs = {}
                fund_kwargs = {}
                try:
                    fund = fund.split(',')
                    fund_kwargs['fund_code'] = fund[0] if fund[0] else ''
                    kwargs['fund_code'] = fund[0] if fund[0] else ''
                    fund_kwargs['fund_name'] = fund[1] if fund[1] else ''
                    fund_kwargs['can_buy'] = True
                    fund_kwargs['pinyin_abbreviation_code'] = fund[2] if fund[2] else ''
                    fund_kwargs['fund_short_name'] = fund[1][:6] if fund[1] else ''
                    kwargs['current_date'] = self.check_date(fund[3])
                    kwargs['current_unit_net_worth'] = self.to_float(fund[4])
                    kwargs['current_cumulative_net_worth'] = self.to_float(fund[5])
                    kwargs['daily'] = self.to_float(fund[6])
                    kwargs['last_week'] = self.to_float(fund[7])
                    kwargs['last_month'] = self.to_float(fund[8])
                    kwargs['last_three_month'] = self.to_float(fund[9])
                    kwargs['last_six_month'] = self.to_float(fund[10])
                    kwargs['last_year'] = self.to_float(fund[11])
                    kwargs['last_two_year'] = self.to_float(fund[12])
                    kwargs['last_three_year'] = self.to_float(fund[13])
                    kwargs['this_year'] = self.to_float(fund[14])
                    kwargs['since_founded'] = self.to_float(fund[15])
                    fund_kwargs['establish_date'] = self.check_date(fund[16], True)
                    kwargs['handling_fee'] = self.to_float(fund[20])
                    fund_kwargs['handling_fee'] = self.to_float(fund[20])
                    fund_historical_networth_ranking_object_list.append(FundHistoricalNetWorthRanking(**kwargs))
                    fund_exists = Fund.objects.filter(fund_code=fund_kwargs['fund_code'])
                    if fund_exists:
                        fund_kwargs.pop('fund_code')
                        fund_kwargs['update_time'] = datetime.now()
                        fund_exists.update(**fund_kwargs)
                    else:
                        fund_object_list.append(Fund(**fund_kwargs))
                except Exception as e:
                    logger.warning("kwargs :{} fund_kwargs: {} error {}".format(kwargs, fund_kwargs, e))
            FundHistoricalNetWorthRanking.objects.bulk_create(fund_historical_networth_ranking_object_list)
            Fund.objects.bulk_create(fund_object_list)
            log_kwargs['end_time'] = datetime.now()
            log_kwargs['total_fund'] = funds_json['allNum']
            log_kwargs['stock_fund_num'] = funds_json['gpNum']
            log_kwargs['hybrid_fund_num'] = funds_json['hhNum']
            log_kwargs['bond_fund_num'] = funds_json['zqNum']
            log_kwargs['index_fund_num'] = funds_json['zsNum']
            log_kwargs['break_even_fund_num'] = funds_json['bbNum']
            log_kwargs['qdii_fund_num'] = funds_json['qdiiNum']
            log_kwargs['etf_fund_num'] = funds_json['etfNum']
            log_kwargs['lof_fund_num'] = funds_json['lofNum']
            log_kwargs['fof_fund_num'] = funds_json['fofNum']
            FundLog.objects.create(**log_kwargs)
        else:
            logger.warning("can not get nodejs server data.")
        logger.info("{} crawl fund ranking completed.".format(datetime.now()))

    def parse_diy_fund_ranking(self):
        logger.info("{} start crawl diy fund ranking".format(datetime.now()))
        url = self.nodejs_server_url + "diy_fund_ranking"
        log_kwargs = {}
        log_kwargs['name'] = '爬取基金从成立以来的净值和分红情况'
        response = requests.get(url)
        funds_json = response.json()
        fund_object_list = []
        fund_historical_networth_ranking_object_list = []
        if funds_json:
            all_fund = funds_json['datas']
            for fund in all_fund:
                fund_kwargs = {}
                kwargs = {}
                try:
                    fund = fund.split(',')
                    fund_kwargs['fund_code'] = fund[0] if fund[0] else ''
                    kwargs['fund_code'] = fund[0] if fund[0] else ''
                    fund_kwargs['fund_name'] = fund[1] if fund[1] else ''
                    fund_kwargs['pinyin_abbreviation_code'] = fund[2] if fund[2] else ''
                    fund_kwargs['fund_short_name'] = fund[1][:6] if fund[1] else ''
                    kwargs['since_founded'] = self.to_float(fund[3])
                    kwargs['since_founded_bonus'] = self.to_float(fund[4])
                    kwargs['since_founded_bonus_num'] = self.to_int(fund[5])
                    fund_kwargs['establish_date'] = self.check_date(fund[6])
                    kwargs['start_unit_net_worth'] = self.to_float(fund[7])
                    kwargs['start_cumulative_net_worth'] = self.to_float(fund[8])
                    kwargs['current_date'] = self.check_date(fund[9])
                    kwargs['current_unit_net_worth'] = self.to_float(fund[10])
                    kwargs['current_cumulative_net_worth'] = self.to_float(fund[11])
                    fund_kwargs['handling_fee'] = fund[14]
                    kwargs['handling_fee'] = fund[14]
                    fund_ranking_exists = FundHistoricalNetWorthRanking.objects.filter(
                        fund_code=kwargs['fund_code'], current_date=kwargs['current_date'])
                    if fund_ranking_exists:
                        kwargs.pop('fund_code')
                        kwargs['update_time'] = datetime.now()
                        fund_ranking_exists.update(**kwargs)
                    else:
                        fund_historical_networth_ranking_object_list.append(FundHistoricalNetWorthRanking(**kwargs))
                    fund_exists = Fund.objects.filter(fund_code=fund_kwargs['fund_code'])
                    if fund_exists:
                        fund_kwargs.pop('fund_code')
                        fund_kwargs['update_time'] = datetime.now()
                        fund_exists.update(**fund_kwargs)
                    else:
                        fund_object_list.append(Fund(**fund_kwargs))
                except Exception as e:
                    logger.warning("kwargs :{} fund_kwargs: {} error {}".format(kwargs, fund_kwargs, e))
            FundHistoricalNetWorthRanking.objects.bulk_create(fund_historical_networth_ranking_object_list)
            Fund.objects.bulk_create(fund_object_list)
            log_kwargs['end_time'] = datetime.now()
            log_kwargs['total_fund'] = funds_json['allNum']
            log_kwargs['stock_fund_num'] = funds_json['gpNum']
            log_kwargs['hybrid_fund_num'] = funds_json['hhNum']
            log_kwargs['bond_fund_num'] = funds_json['zqNum']
            log_kwargs['index_fund_num'] = funds_json['zsNum']
            log_kwargs['break_even_fund_num'] = funds_json['bbNum']
            log_kwargs['qdii_fund_num'] = funds_json['qdiiNum']
            log_kwargs['etf_fund_num'] = funds_json['etfNum']
            log_kwargs['lof_fund_num'] = funds_json['lofNum']
        else:
            logger.warning("get div_fund_ranking json data error!")
        logger.info("{} crawl diy fund ranking completed.".format(datetime.now()))

    def get_history_net_worth(self):
        fund_codes = Fund.objects.all().values(['fund_code'])

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
        # 日期时间转换，将 09-17 转为 2020-09-17

    def format_datetime(self, val):
        try:
            if val:
                print(val)
                val = str(datetime.now().year) + "-" + val
                val = datetime.strptime(val, '%Y-%m-%d')
                return val
            return str(datetime.now())
        except Exception as e:
            val = self.date
            logger.warning("format date error {} --- {}".format(val, e))
            return val

    def check_date(self, val, can_null=False):
        try:
            val = val.replace('---', '').replace('--', '')
            if val and isinstance(datetime.strptime(val, '%Y-%m-%d'), datetime):
                return val
            return '' if can_null else self.date
        except Exception as e:
            logger.warning("check date failed! val :{} -- {}".format(val, e))
            return '' if can_null else self.date


if __name__ == '__main__':
    easymoney = EastMoneyFund()
