import logging
from datetime import datetime
from urllib.parse import urlencode
import threading
import requests
import os
from apps.Fund.models import FundHistoricalNetWorthRanking, FundLog, Fund, FundCompany

logger = logging.getLogger("easymoneyfundcrawler")


# 东方财富基金
class EastMoneyFund:
    nodejs_server_url = 'http://127.0.0.1:3000?type='
    # 当天日期
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    # 默认错误日期，当日期处理错误时候，将日期设置为 这个值
    default_error_date = '1976-01-01'
    # 默认基金历史数据最大条数
    default_history_fund_max_size = 50 * 365
    # 默认最大基金数
    default_max_fund_num = 100000
    # 默认线程数
    thread_num = 50

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        'Referer': "http://fund.eastmoney.com/data/diyfundranking.html",
        'Host': "fund.eastmoney.com",
        'Cookie': 'em_hq_fls=js; qgqp_b_id=9715e29311d3fc5888ee05d9afbfcb92; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; waptgshowtime=2020917; st_si=25027075577965; ASP.NET_SessionId=t1vuewxy0cbz5wgyu2adoib5; HAList=a-sz-002127-%u5357%u6781%u7535%u5546%2Cd-hk-06862%2Ca-sz-000066-%u4E2D%u56FD%u957F%u57CE%2Cf-0-399006-%u521B%u4E1A%u677F%u6307; cowCookie=true; intellpositionL=1215.35px; st_asi=delete; intellpositionT=499.8px; searchbar_code=320007; EMFUND1=09-19%2013%3A04%3A14@%23%24%u9E4F%u626C%u5229%u6CA3%u77ED%u503AE@%23%24006831; EMFUND0=09-19%2001%3A35%3A46@%23%24%u5609%u5B9E%u589E%u957F%u6DF7%u5408@%23%24070002; EMFUND2=09-19%2013%3A42%3A08@%23%24%u519C%u94F6%u65B0%u80FD%u6E90%u4E3B%u9898@%23%24002190; EMFUND3=09-19%2016%3A40%3A24@%23%24%u94F6%u6CB3%u521B%u65B0%u6210%u957F%u6DF7%u5408@%23%24519674; EMFUND4=09-19%2016%3A50%3A54@%23%24%u4E2D%u878D%u4EA7%u4E1A%u5347%u7EA7%u6DF7%u5408@%23%24001701; EMFUND5=09-19%2022%3A34%3A36@%23%24%u5357%u534E%u745E%u626C%u7EAF%u503AC@%23%24005048; EMFUND6=09-19%2021%3A51%3A18@%23%24%u5DE5%u94F6%u65B0%u8D8B%u52BF%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408A@%23%24001716; EMFUND7=09-19%2022%3A36%3A19@%23%24%u534E%u5B89%u521B%u4E1A%u677F50%u6307%u6570%u5206%u7EA7B@%23%24150304; EMFUND9=09-20%2010%3A03%3A59@%23%24%u8BFA%u5B89%u6210%u957F%u6DF7%u5408@%23%24320007; EMFUND8=09-20 10:24:15@#$%u5B89%u4FE1%u6C11%u7A33%u589E%u957F%u6DF7%u5408C@%23%24008810; st_pvi=58947008966039; st_sp=2020-07-25%2000%3A32%3A56; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=294; st_psi=20200920102414487-0-3267835636',
    }
    # history_net_worth_url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18306004163724110205_1600526195568&fundCode=150304&pageIndex=61&pageSize=20&startDate=&endDate=&_=1600569328705'
    history_net_worth_url = 'http://api.fund.eastmoney.com/f10/lsjz?'
    fund_company_url = 'http://fund.eastmoney.com/Company/default.html'

    def __init__(self):
        self.parse_fund_ranking()
        self.parse_diy_fund_ranking()
        self.schedule_history_net_worth()
        self.get_fund_company()

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
                    pass
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
            pass
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
                    fund_kwargs['handling_fee'] = self.to_float(fund[14])
                    kwargs['handling_fee'] = self.to_float(fund[14])
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
                    pass
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
            pass
        logger.info("{} crawl diy fund ranking completed.".format(datetime.now()))

    def schedule_history_net_worth(self):
        fund_codes = Fund.objects.all().values('fund_code')
        fund_codes = [x['fund_code'] for x in fund_codes]
        fund_code_task_list = self.split_list(fund_codes, self.thread_num)
        for task in fund_code_task_list:
            t = threading.Thread(target=self.parse_history_net_worth, args=(task,))
            t.start()
            t.join()

    def parse_history_net_worth(self, fund_codes):
        logger.info("thread {} {} start crawl history net worth .".format(os.getpid(), datetime.now()))
        for fund_code in fund_codes:
            params = {
                'fundCode': fund_code,
                'pageIndex': 1,
                'pageSize': self.default_history_fund_max_size,
                '_': '1600569328705',
            }
            fund_history_object_list = []
            request_url = self.history_net_worth_url + urlencode(params)
            response = requests.get(request_url, headers=self.headers)
            history_net_worth_json = response.json()
            if history_net_worth_json and history_net_worth_json.get('Data').get('LSJZList'):
                history_net_worths = history_net_worth_json.get('Data').get('LSJZList')
                for history_net_worth in history_net_worths:
                    try:
                        kwargs = {'fund_code': fund_code}
                        kwargs['current_date'] = self.check_date(history_net_worth['FSRQ'])
                        kwargs['current_unit_net_worth'] = self.to_float(history_net_worth['DWJZ'])
                        kwargs['current_cumulative_net_worth'] = self.to_float(history_net_worth['LJJZ'])
                        kwargs['daily'] = self.to_float(history_net_worth['JZZZL'])
                        kwargs['subscription_status'] = history_net_worth['SGZT']
                        kwargs['redemption_status'] = history_net_worth['SHZT']
                        kwargs['dividend_distribution'] = history_net_worth['FHSP']
                        fund_exists = FundHistoricalNetWorthRanking.objects.filter(
                            fund_code=kwargs['fund_code'], current_date=kwargs['current_date'])
                        if fund_exists:
                            kwargs.pop('fund_code')
                            kwargs['update_time'] = datetime.now()
                            fund_exists.update(**kwargs)
                        else:
                            fund_history_object_list.append(FundHistoricalNetWorthRanking(**kwargs))
                    except Exception as e:
                        logger.warning("{} get history_net_worth error ! fund_code: {} kwargs: {}".format(
                            datetime.now(), fund_code, kwargs))
                        pass
            FundHistoricalNetWorthRanking.objects.bulk_create(fund_history_object_list)
        logger.info("thread {} {} crawl history net worth complete.".format(os.getpid(), datetime.now()))

    def get_fund_company(self):
        logger.info("{} start crawl fund company .".format(datetime.now()))
        url = self.nodejs_server_url + "fund_company"
        response = requests.get(url)
        funds_company_json = response.json()
        funds_company_object_list = []
        if funds_company_json and funds_company_json.get('datas'):
            funds_company = funds_company_json.get('datas')
            for company in funds_company:
                kwargs = {}
                try:
                    kwargs['company_id'] = company[0] if company[0] else ''
                    kwargs['company_name'] = company[1] if company[1] else ''
                    kwargs['establish_date'] = self.check_date(company[2])
                    kwargs['total_fund_num'] = self.to_int(company[3])
                    kwargs['general_manager'] = company[4] if company[4] else ''
                    kwargs['pinyin_abbreviation_code'] = company[5] if company[5] else ''
                    kwargs['total_manage_amount'] = self.to_float(company[7])
                    kwargs['tianxiang_star'] = len(company[8]) if company[8] else 0
                    kwargs['company_short_name'] = company[9] if company[9] else ''
                    if company[11]:
                        update_date = company[11].split(' ')
                        update_date = update_date[0].replace('/', '-')
                        update_date = self.check_date(update_date)
                        kwargs['update_date'] = update_date
                    else:
                        kwargs['update_date'] = self.default_error_date
                    is_exist = FundCompany.objects.filter(company_id=kwargs['company_id'])
                    if is_exist:
                        kwargs.pop('company_id')
                        kwargs['update_time'] = datetime.now()
                        FundCompany.objects.update(**kwargs)
                    else:
                        funds_company_object_list.append(FundCompany(**kwargs))
                except Exception as e:
                    logger.warning("{} parse fund compny error! {} -{} {}".format(datetime.now(), company, kwargs, e))
            FundCompany.objects.bulk_create(funds_company_object_list)
        else:
            logger.warning("{} can not get fund company! perhaps nodejs crawl server not "
                           "started.".format(datetime.now()))
        logger.info("{} crawl fund company complete.".format(datetime.now()))

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
                val = str(datetime.now().year) + "-" + val
                val = datetime.strptime(val, '%Y-%m-%d')
                return val
            return self.default_error_date
        except Exception as e:
            logger.warning("format date error {} --- {}".format(val, e))
            return self.default_error_date

    def check_date(self, val, can_null=False):
        try:
            val = val.replace('---', '').replace('--', '')
            if val and isinstance(datetime.strptime(val, '%Y-%m-%d'), datetime):
                return val
            return '' if can_null else self.default_error_date
        except Exception as e:
            logger.warning("check date failed! val :{} -- {}".format(val, e))
            return '' if can_null else self.default_error_date

    def split_list(self, list, n):
        target_list = []
        cut = int(len(list) / n)
        if cut == 0:
            list = [[x] for x in list]
            none_array = [[] for i in range(0, n - len(list))]
            return list + none_array
        for i in range(0, n - 1):
            target_list.append(list[cut * i:cut * (1 + i)])
        target_list.append(list[cut * (n - 1):len(list)])
        return target_list


if __name__ == '__main__':
    easymoney = EastMoneyFund()
