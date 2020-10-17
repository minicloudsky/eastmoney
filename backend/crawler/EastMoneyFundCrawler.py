import copy
import logging
import threading
import time
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlencode
from django.db import transaction
from django.conf import settings
import requests

from apps.fund.models import FundManagerRelationship, FundRanking, FundHistoricalNetWorth, FundLog, Fund, FundCompany, \
    FundManager, FundTask
from utils.decorators import log

logger = logging.getLogger("easymoneyfundcrawler")


# 东方财富基金
class EastMoneyFund:
    nodejs_server_url = 'http://127.0.0.1:3000?type='
    # 当天日期
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    # 默认错误日期，当日期处理错误时候，将日期设置为 这个值
    default_error_date = datetime.strptime('1976-01-01', '%Y-%m-%d')
    crawl_mode = settings.CRAWL_MODE
    # 默认基金历史数据最大条数,全量时爬取 50年数据，增量时爬取最近 10 天数据
    default_history_fund_max_size = 50 * 365 if crawl_mode == 'ALL' else 10
    # 默认最大基金数
    default_max_fund_num = 100000
    # 默认线程数
    thread_num = 75
    # 基金总数
    total_fund = 0
    mutex = threading.Lock()
    crawl_history_task = None
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        'Referer': "http://fund.eastmoney.com/data/diyfundranking.html",
        'Host': "fund.eastmoney.com",
        'Cookie': 'em_hq_fls=js; qgqp_b_id=9715e29311d3fc5888ee05d9afbfcb92; AUTH_FUND.EASTMONEY.COM_GSJZ=AUTH*TTJJ*TOKEN; waptgshowtime=2020917; st_si=25027075577965; ASP.NET_SessionId=t1vuewxy0cbz5wgyu2adoib5; HAList=a-sz-002127-%u5357%u6781%u7535%u5546%2Cd-hk-06862%2Ca-sz-000066-%u4E2D%u56FD%u957F%u57CE%2Cf-0-399006-%u521B%u4E1A%u677F%u6307; cowCookie=true; intellpositionL=1215.35px; st_asi=delete; intellpositionT=499.8px; searchbar_code=320007; EMFUND1=09-19%2013%3A04%3A14@%23%24%u9E4F%u626C%u5229%u6CA3%u77ED%u503AE@%23%24006831; EMFUND0=09-19%2001%3A35%3A46@%23%24%u5609%u5B9E%u589E%u957F%u6DF7%u5408@%23%24070002; EMFUND2=09-19%2013%3A42%3A08@%23%24%u519C%u94F6%u65B0%u80FD%u6E90%u4E3B%u9898@%23%24002190; EMFUND3=09-19%2016%3A40%3A24@%23%24%u94F6%u6CB3%u521B%u65B0%u6210%u957F%u6DF7%u5408@%23%24519674; EMFUND4=09-19%2016%3A50%3A54@%23%24%u4E2D%u878D%u4EA7%u4E1A%u5347%u7EA7%u6DF7%u5408@%23%24001701; EMFUND5=09-19%2022%3A34%3A36@%23%24%u5357%u534E%u745E%u626C%u7EAF%u503AC@%23%24005048; EMFUND6=09-19%2021%3A51%3A18@%23%24%u5DE5%u94F6%u65B0%u8D8B%u52BF%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408A@%23%24001716; EMFUND7=09-19%2022%3A36%3A19@%23%24%u534E%u5B89%u521B%u4E1A%u677F50%u6307%u6570%u5206%u7EA7B@%23%24150304; EMFUND9=09-20%2010%3A03%3A59@%23%24%u8BFA%u5B89%u6210%u957F%u6DF7%u5408@%23%24320007; EMFUND8=09-20 10:24:15@#$%u5B89%u4FE1%u6C11%u7A33%u589E%u957F%u6DF7%u5408C@%23%24008810; st_pvi=58947008966039; st_sp=2020-07-25%2000%3A32%3A56; st_inirUrl=https%3A%2F%2Fwww.eastmoney.com%2F; st_sn=294; st_psi=20200920102414487-0-3267835636',
    }
    # history_net_worth_url = 'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18306004163724110205_1600526195568&fundCode=150304&pageIndex=61&pageSize=20&startDate=&endDate=&_=1600569328705'
    history_net_worth_url = 'http://api.fund.eastmoney.com/f10/lsjz?'
    fund_company_url = 'http://fund.eastmoney.com/Company/default.html'
    monetary_fund_url = 'http://api.fund.eastmoney.com/FundRank/GetHbRankList?intCompany=0&MinsgType=&IsSale=0&strSortCol=SYL_Y&orderType=desc&pageIndex=1&pageSize=500000&_=1601519558625'
    asset_manage_fund_url = 'http://api.fund.eastmoney.com/FundRank/GetLcRankList?intCompany=0&MinsgType=undefined' \
                            '&IsSale=0&strSortCol=SYL_Z&orderType=desc&pageIndex={}&pageSize={}&FBQ='.format(
        1, 500000)
    overseas_fund_url = 'http://overseas.1234567.com.cn/overseasapi/OpenApiHander.ashx?api=HKFDApi&m=MethodFundList&action=1&pageindex={}&pagesize={}&dy=1&date1=1990-10-02&date2={}&sortfield=W&sorttype=-1&isbuy=0'

    def __init__(self):
        FundLog.objects.create(
            name="开始爬取, 当前爬取模式为 {}".format(self.crawl_mode),
            start_time=datetime.now(), end_time=datetime.now())
        thread_list_first = [
            threading.Thread(target=self.get_fund_company),
            threading.Thread(target=self.parse_fund_ranking),
            threading.Thread(target=self.parse_diy_fund_ranking),
            threading.Thread(target=self.get_monetary_fund_ranking),
            threading.Thread(target=self.get_asset_manage_fund_ranking),
            threading.Thread(target=self.get_fbs_fund_ranking),
            threading.Thread(target=self.get_hongkong_fund_ranking),
        ]
        for t in thread_list_first:
            t.start()
        for t in thread_list_first:
            t.join()
        thread_list_second = [
            threading.Thread(target=self.schedule_history_net_worth),
            # threading.Thread(target=self.single_thread_parse_history_net_worth),
            threading.Thread(target=self.get_fund_manager),
            threading.Thread(target=self.update_fund_type),
        ]
        for t in thread_list_second:
            t.start()
        for t in thread_list_second:
            t.join()
        logger.warning(
            "------{} All crawling task finished".format(datetime.now()))
        FundLog.objects.create(
            name="爬取东方财富基金数据完成", start_time=datetime.now(), end_time=datetime.now())

    @log("{} 爬取基金排行".format(datetime.now()))
    def parse_fund_ranking(self):
        url = self.nodejs_server_url + "fund_ranking"
        log_kwargs = {}
        log_kwargs['name'] = '爬取基金排行'
        log_kwargs['start_time'] = datetime.now()
        response = self.get(url)
        funds_json = copy.copy(response.json())
        if funds_json:
            all_fund = copy.copy(funds_json['datas'])
            for fund in all_fund:
                defaults = {}
                fund_defaults = {}
                try:
                    fund = fund.split(',')
                    fund_code = fund[0] if fund[0] else ''
                    fund_defaults['fund_name'] = fund[1] if fund[1] else ''
                    fund_defaults['can_buy'] = True
                    fund_defaults['pinyin_abbreviation_code'] = fund[2] if fund[2] else ''
                    fund_defaults['fund_short_name'] = fund[1][:6] if fund[1] else ''
                    current_date = self.check_date(fund[3])
                    defaults['current_unit_net_worth'] = self.to_float(fund[4])
                    defaults['current_cumulative_net_worth'] = self.to_float(
                        fund[5])
                    defaults['daily'] = self.to_float(fund[6])
                    defaults['last_week'] = self.to_float(fund[7])
                    defaults['last_month'] = self.to_float(fund[8])
                    defaults['last_three_month'] = self.to_float(fund[9])
                    defaults['last_six_month'] = self.to_float(fund[10])
                    defaults['last_year'] = self.to_float(fund[11])
                    defaults['last_two_year'] = self.to_float(fund[12])
                    defaults['last_three_year'] = self.to_float(fund[13])
                    defaults['this_year'] = self.to_float(fund[14])
                    defaults['since_founded'] = self.to_float(fund[15])
                    fund_defaults['establish_date'] = self.check_date(
                        fund[16], True)
                    defaults['handling_fee'] = self.to_float(fund[20])
                    fund_defaults['handling_fee'] = self.to_float(fund[20])
                    fund_defaults['update_time'] = datetime.now()
                    defaults['update_time'] = datetime.now()
                    with transaction.atomic():
                        FundRanking.objects.update_or_create(
                            defaults=defaults, **{'fund_code': fund_code, 'current_date': current_date})
                    with transaction.atomic():
                        Fund.objects.update_or_create(
                            defaults=fund_defaults, **{'fund_code': fund_code})
                        # FundHistoricalNetWorthRanking.objects.update_or_create(
                        #     defaults=defaults, **{'fund_code': fund_code, 'current_date': current_date})
                        # fund.objects.update_or_create(
                        #     defaults=fund_defaults, **{'fund_code': fund_code})
                except Exception as e:
                    logger.warning("kwargs :{} fund_kwargs: {} error {}".format(
                        defaults, fund_defaults, e))
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

    @log("{} 爬取自定义基金排行".format(datetime.now()))
    def parse_diy_fund_ranking(self):
        url = self.nodejs_server_url + "diy_fund_ranking"
        log_kwargs = {}
        log_kwargs['name'] = '爬取基金从成立以来的净值和分红情况'
        response = self.get(url)
        funds_json = copy.copy(response.json())
        if funds_json:
            all_fund = funds_json['datas']
            for fund in all_fund:
                fund_defaults = {}
                defaults = {}
                try:
                    fund = fund.split(',')
                    fund_code = fund[0] if fund[0] else ''
                    current_date = self.check_date(fund[9])
                    fund_defaults['fund_name'] = fund[1] if fund[1] else ''
                    fund_defaults['pinyin_abbreviation_code'] = fund[2] if fund[2] else ''
                    fund_defaults['fund_short_name'] = fund[1][:6] if fund[1] else ''
                    defaults['since_founded'] = self.to_float(fund[3])
                    defaults['since_founded_bonus'] = self.to_float(fund[4])
                    defaults['since_founded_bonus_num'] = self.to_int(fund[5])
                    fund_defaults['establish_date'] = self.check_date(fund[6])
                    defaults['start_unit_net_worth'] = self.to_float(fund[7])
                    defaults['start_cumulative_net_worth'] = self.to_float(
                        fund[8])
                    defaults['current_unit_net_worth'] = self.to_float(
                        fund[10])
                    defaults['current_cumulative_net_worth'] = self.to_float(
                        fund[11])
                    fund_defaults['handling_fee'] = self.to_float(fund[14])
                    defaults['handling_fee'] = self.to_float(fund[14])
                    defaults['update_time'] = datetime.now()
                    fund_defaults['update_time'] = datetime.now()
                    with transaction.atomic():
                        FundRanking.objects.update_or_create(
                            defaults=defaults, **{'fund_code': fund_code, 'current_date': current_date})
                    with transaction.atomic():
                        Fund.objects.update_or_create(
                            defaults=fund_defaults, **{'fund_code': fund_code})
                except Exception as e:
                    logger.warning("kwargs :{} fund_kwargs: {} error {}".format(
                        defaults, fund_defaults, e))
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
        logger.info(
            "{} crawl diy fund ranking completed.".format(datetime.now()))
        FundLog.objects.create(
            name="爬取自定义基金排行完成", start_time=datetime.now(), end_time=datetime.now())

    @log("{} 爬取基金历史净值".format(datetime.now()))
    def schedule_history_net_worth(self):
        with transaction.atomic():
            funds = Fund.objects.all()
            fund_codes = [
                fund.fund_code for fund in funds if fund.fund_type != 'HK']
        logger.info("total funds: {}".format(len(fund_codes)))
        self.total_fund = len(fund_codes)
        self.crawl_history_task = FundTask.objects.create(
            func='multi_thread_parse_history_net_worth', name="多线程爬取基金历史净值", status='running')
        pool = ThreadPool(self.thread_num)
        # 在每个线程中执行任务
        thread_exec_results = pool.map(
            self.parse_history_net_worth, fund_codes)
        # Close the pool and wait for the work to finish
        pool.close()
        pool.join()
        self.crawl_history_task.name = "单线程爬取基金历史净值爬取结束"
        self.crawl_history_task.update_time = datetime.now()
        self.crawl_history_task.save()

    @log("{} 单线程爬取基金历史净值".format(datetime.now()))
    def single_thread_parse_history_net_worth(self):
        with transaction.atomic():
            funds = Fund.objects.all()
            fund_codes = [
                fund.fund_code for fund in funds if fund.fund_type != 'HK']
        total = len(fund_codes)
        log = FundTask.objects.create(
            func='single_thread_parse_history_net_worth', name="单线程爬取基金历史净值", status='running')
        for fund_code in fund_codes:
            self.parse_history_net_worth(fund_code)
            total -= 1
            logger.warning(
                "单线程爬取基金历史净值,已爬取 {} 历史净值，剩余基金数 {}".format(fund_code, total))
            log.name = "单线程爬取基金历史净值,已爬取 {} 历史净值，剩余基金数 {}".format(
                fund_code, total)
            log.status = 'running'
            log.save()
        log.name = "单线程爬取基金历史净值已经完成"
        log.status = 'completed'
        log.update_time = datetime.now()
        log.save()

    def parse_history_net_worth(self, fund_code):
        crawl_start_time = time.time()
        params = {
            'fundCode': fund_code,
            'pageIndex': 1,
            'pageSize': self.default_history_fund_max_size,
            '_': '1600569328705',
        }
        request_url = self.history_net_worth_url + urlencode(params)
        response = self.get(request_url)
        history_net_worth_json = copy.copy(response.json())
        if history_net_worth_json and history_net_worth_json.get('Data').get('LSJZList'):
            history_net_worths = history_net_worth_json.get(
                'Data').get('LSJZList')
            fund_history_obj_list = []
            for history_net_worth in history_net_worths:
                defaults = {}
                try:
                    current_date = self.check_date(history_net_worth['FSRQ'])
                    defaults['current_unit_net_worth'] = self.to_float(
                        history_net_worth['DWJZ'])
                    defaults['current_cumulative_net_worth'] = self.to_float(
                        history_net_worth['LJJZ'])
                    defaults['daily'] = self.to_float(
                        history_net_worth['JZZZL'])
                    defaults['subscription_status'] = history_net_worth['SGZT']
                    defaults['redemption_status'] = history_net_worth['SHZT']
                    defaults['dividend_distribution'] = history_net_worth['FHSP']
                    defaults['update_time'] = datetime.now()
                    kwargs = {'fund_code': fund_code, 'current_date': current_date}
                    with transaction.atomic():
                        exist_history_fund = FundHistoricalNetWorth.objects.filter(
                            **kwargs)
                        if exist_history_fund:
                            exist_history_fund.update(**defaults)
                        else:
                            defaults.update(kwargs)
                            fund_history_obj_list.append(FundHistoricalNetWorth(**defaults))
                except Exception as e:
                    logger.warning("{} get history_net_worth error ! fund_code: {} kwargs: {} exception : {}".format(
                        datetime.now(), fund_code, defaults, e))
            with transaction.atomic():
                FundHistoricalNetWorth.objects.bulk_create(fund_history_obj_list)
            self.total_fund -= 1
            crawl_end_time = time.time()
            self.crawl_history_task.name = "多线程爬取基金历史净值,当前线程 {} -已爬取 {} 历史净值，剩余基金数 {},本次用时 {} s,预计爬完还需要 {} hour".format(
                threading.current_thread().getName(),
                fund_code, self.total_fund, crawl_end_time - crawl_start_time,
                                            (crawl_end_time - crawl_start_time) * self.total_fund / 3600)
            self.crawl_history_task.update_time = datetime.now()
            with transaction.atomic():
                self.crawl_history_task.save()

    @log("{} 爬取基金公司".format(datetime.now()))
    def get_fund_company(self):
        url = self.nodejs_server_url + "fund_company"
        response = self.get(url)
        funds_company_json = response.json()
        funds_company_object_list = []
        if funds_company_json and funds_company_json.get('datas'):
            funds_company = funds_company_json.get('datas')
            for company in funds_company:
                defaults = {}
                try:
                    company_id = company[0] if company[0] else ''
                    defaults['company_name'] = company[1] if company[1] else ''
                    defaults['establish_date'] = self.check_date(company[2])
                    defaults['total_fund_num'] = self.to_int(company[3])
                    defaults['general_manager'] = company[4] if company[4] else ''
                    defaults['pinyin_abbreviation_code'] = company[5] if company[5] else ''
                    defaults['total_manage_amount'] = self.to_float(company[7])
                    defaults['tianxiang_star'] = len(
                        company[8]) if company[8] else 0
                    defaults['company_short_name'] = company[9] if company[9] else ''
                    if company[11]:
                        update_date = company[11].split(' ')
                        update_date = update_date[0].replace('/', '-')
                        update_date = self.check_date(update_date)
                        defaults['update_date'] = update_date
                        defaults['update_time'] = datetime.now()
                    else:
                        defaults['update_date'] = self.default_error_date
                    FundCompany.objects.update_or_create(defaults=defaults,
                                                         **{'company_id': company_id})
                except Exception as e:
                    logger.warning(
                        "{} parse fund compny error! {} -{} {}".format(datetime.now(), company, defaults, e))
            FundCompany.objects.bulk_create(funds_company_object_list)
        else:
            logger.warning("{} can not get fund company! perhaps nodejs crawl server not "
                           "started.".format(datetime.now()))

    @log("{} 爬取场内交易基金".format(datetime.now()))
    def get_fbs_fund_ranking(self):
        url = self.nodejs_server_url + "fbs_fund_ranking"
        response = self.get(url)
        fbs_funds = response.json()
        if not fbs_funds['datas']:
            logger.warning("get_fbs_fund_ranking empty data.")
            return
        all_fbs_funds = fbs_funds['allRecords']
        logger.info("场内交易基金总数: {}".format(all_fbs_funds))
        for fbs_fund in fbs_funds['datas']:
            try:
                fbs_fund = fbs_fund.split(',')
                fund_code = fbs_fund[0] if fbs_fund[0] else ''
                current_date = self.check_date(
                    fbs_fund[3]) if fbs_fund[3] else ''
                fund_defaults = {
                    'fund_name': fbs_fund[1] if fbs_fund[1] else '',
                    'pinyin_abbreviation_code': fbs_fund[2] if fbs_fund[2] else '',
                    'fund_type': fbs_fund[-2] if fbs_fund[-2] else '',
                    'establish_date': self.check_date(fbs_fund[15]) if fbs_fund[15] else '',
                    'update_time': datetime.now(),
                }
                defaults = {
                    'current_unit_net_worth': self.to_float(fbs_fund[4]),
                    'current_cumulative_net_worth': self.to_float(fbs_fund[5]),
                    'last_week': self.to_float(fbs_fund[6]),
                    'last_month': self.to_float(fbs_fund[7]),
                    'last_three_month': self.to_float(fbs_fund[8]),
                    'last_six_month': self.to_float(fbs_fund[9]),
                    'last_year': self.to_float(fbs_fund[10]),
                    'last_two_year': self.to_float(fbs_fund[11]),
                    'last_three_year': self.to_float(fbs_fund[12]),
                    'this_year': self.to_float(fbs_fund[13]),
                    'since_founded': self.to_float(fbs_fund[14]),
                    'update_time': datetime.now(),
                }
                with transaction.atomic():
                    Fund.objects.update_or_create(defaults=fund_defaults, **{'fund_code': fund_code})
                with transaction.atomic():
                    FundRanking.objects.update_or_create(
                        defaults=defaults, **{'fund_code': fund_code, 'current_date': current_date})
            except Exception as e:
                logger.warning("get fbs fund error {}".format(e))
                pass

    @log("{} 爬取货币基金排行".format(datetime.now()))
    def get_monetary_fund_ranking(self):
        response = self.get(self.monetary_fund_url)
        datas = response.json()
        if not datas:
            logger.warning("货币基金数据为空!")
            return
        logger.warning("货币基金总数: {}".format(datas['TotalCount']))
        for fund in datas['Data']:
            try:
                fund_code = fund['FCODE'] if fund['FCODE'] else ''
                current_date = self.check_date(
                    fund['FSRQ']) if fund['FSRQ'] else self.default_error_date
                fund_defaults = {
                    'fund_name': fund['SHORTNAME'],
                    'pinyin_abbreviation_code': fund['ABBNAME'],
                    'can_buy': 1 if fund['ISBUY'] == 1 else 0,
                    'fund_type': fund['FTYPE'],
                    'update_time': datetime.now(),
                    'establish_date': self.default_error_date,
                }
                defaults = {
                    'ten_thousand_income': self.to_float(fund['DWJZ']),
                    'annualized_income_7day': self.to_float(fund['LJJZ']),
                    'annualized_income_14day': self.to_float(fund['FTYI']),
                    'annualized_income_28day': self.to_float(fund['TEYI']),
                    'current_unit_net_worth': self.to_float(fund['JZ']),
                    'last_month': self.to_float(fund['SYL_Y']),
                    'last_three_month': self.to_float(fund['SYL_3Y']),
                    'last_six_month': self.to_float(fund['SYL_6Y']),
                    'last_year': self.to_float(fund['SYL_1N']),
                    'last_two_year': self.to_float(fund['SYL_2N']),
                    'last_three_year': self.to_float(fund['SYL_3N']),
                    'last_five_year': self.to_float(fund['SYL_5N']),
                    'this_year': self.to_float(fund['SYL_JN']),
                    'since_founded': self.to_float(fund['SYL_LN']),
                    'handling_fee': self.to_float(fund['RATE']),
                }
                with transaction.atomic():
                    Fund.objects.update_or_create(defaults=fund_defaults,
                                                  **{'fund_code': fund_code})
                with transaction.atomic():
                    FundRanking.objects.update_or_create(
                        defaults=defaults, **{'fund_code': fund_code,
                                              'current_date': current_date})
            except Exception as e:
                logger.warning("exception in monetary_fund : {}".format(e))
                pass

    @log("{} 爬取理财基金排行".format(datetime.now()))
    def get_asset_manage_fund_ranking(self):
        response = self.get(self.asset_manage_fund_url)
        datas = response.json()
        if not datas:
            logger.warning("理财基金数据为空!")
            return
        logger.warning("理财基金总数: {}".format(datas['TotalCount']))
        for fund in datas['Data']:
            try:
                fund_code = fund['FCODE'] if fund['FCODE'] else ''
                current_date = self.check_date(
                    fund['FSRQ']) if fund['FSRQ'] else self.default_error_date
                fund_defaults = {
                    'fund_name': fund['SHORTNAME'],
                    'pinyin_abbreviation_code': fund['ABBNAME'],
                    'can_buy': 1 if fund['ISBUY'] == 1 else 0,
                    'fund_type': fund['FTYPE'],
                    'update_time': datetime.now(),
                    'establish_date': self.default_error_date,
                }
                defaults = {
                    'ten_thousand_income': self.to_float(fund['DWJZ']),
                    'annualized_income_7day': self.to_float(fund['LJJZ']),
                    'annualized_income_14day': self.to_float(fund['FTYI']),
                    'annualized_income_28day': self.to_float(fund['TEYI']),
                    'current_unit_net_worth': self.to_float(fund['JZ']),
                    'last_month': self.to_float(fund['SYL_Y']),
                    'last_three_month': self.to_float(fund['SYL_3Y']),
                    'last_six_month': self.to_float(fund['SYL_6Y']),
                    'this_year': self.to_float(fund['SYL_JN']),
                    'since_founded': self.to_float(fund['SYL_LN']),
                    'handling_fee': self.to_float(fund['RATE']),
                }
                with transaction.atomic():
                    Fund.objects.update_or_create(
                        defaults=fund_defaults, **{'fund_code': fund_code})
                with transaction.atomic():
                    FundRanking.objects.update_or_create(
                        defaults=defaults, **{'fund_code': fund_code, 'current_date': current_date})
            except Exception as e:
                logger.warning("exception in asset manage fund : {}".format(e))
                pass

    @log("{} 爬取香港基金排行".format(datetime.now()))
    def get_hongkong_fund_ranking(self):
        try:
            response = self.get(
                self.overseas_fund_url.format(1, 50, self.date))
            datas = response.json()
            if not datas:
                logger.warning("香港基金数据为空!")
                return
            logger.warning("香港基金总数: {}".format(datas['TotalCount']))
        except Exception as e:
            logger.warning("Exception in get hk fund {}".format(e))
            return
        total_page = datas['TotalCount'] / 50 + \
                     1 if datas['TotalCount'] else 10
        for page in range(int(total_page) + 1):
            response = self.get(
                self.overseas_fund_url.format(page, 50, self.date))
            try:
                datas = response.json()
            except Exception as e:
                logger.warning("Exception in get hk fund {}".format(e))
                datas = None
            if not datas:
                break
            for fund in datas['Data']:
                if not datas:
                    logger.warning("香港基金数据为空!")
                    return
                try:
                    fund_code = fund['FCODE'] if fund['FCODE'] else ''
                    current_date = self.check_date(
                        fund['JZRQ']) if fund['JZRQ'] else self.default_error_date
                    fund_defaults = {
                        'fund_name': fund['FULLNAME'],
                        'fund_short_name': fund['SHORTNAME'],
                        'can_buy': 1 if fund['ISBUY'] == 1 else 0,
                        'fund_type': 'HK',
                        'currency': fund['CURRENCY'] if fund['CURRENCY'] else '',
                        'update_time': datetime.now(),
                        'establish_date': self.default_error_date,
                    }
                    defaults = {
                        'last_week': self.to_float(fund['W']),
                        'current_unit_net_worth': self.to_float(fund['NAV']),
                        'last_month': self.to_float(fund['M']),
                        'last_three_month': self.to_float(fund['Q']),
                        'last_six_month': self.to_float(fund['HY']),
                        'last_year': self.to_float(fund['Y']),
                        'last_two_year': self.to_float(fund['TWY']),
                        'last_three_year': self.to_float(fund['TRY']),
                        'this_year': self.to_float(fund['SY']),
                        'since_founded': self.to_float(fund['SE']),
                    }
                    with transaction.atomic():
                        Fund.objects.update_or_create(
                            defaults=fund_defaults, **{'fund_code': fund_code})
                    with transaction.atomic():
                        FundRanking.objects.update_or_create(
                            defaults=defaults, **{'fund_code': fund_code, 'current_date': current_date})
                except Exception as e:
                    logger.warning("exception in hk fund : {}".format(e))
                    pass

    @log("{} 爬取基金经理".format(datetime.now()))
    def get_fund_manager(self):
        request_url = self.nodejs_server_url + "fund_manager"
        response = self.get(request_url)
        datas = response.json()
        total_manager = datas['record']
        logger.warning("基金经理总数: {}".format(total_manager))
        managers = datas['data']
        fund_manager_objs = []
        for manager in managers:
            try:
                defaults = {}
                manager_id = manager[0] if manager[0] else 0
                name = manager[1] if manager[1] else '',
                company_id = manager[2] if manager[2] else 0,
                managed_funds = manager[4].split(',') if manager[4] else ''
                relationship_objs = []
                for fund_code in managed_funds:
                    relationship = {
                        'fund_code': fund_code,
                        'manager_id': manager_id,
                        'update_time': datetime.now(),
                    }
                    exist_relationship = FundManagerRelationship.objects.filter(
                        **{'fund_code': fund_code, 'manager_id': manager_id, })
                    if exist_relationship:
                        exist_relationship.update(**relationship)
                    else:
                        relationship.update(
                            **{'fund_code': fund_code, 'manager_id': manager_id, })
                        relationship_objs.append(
                            FundManagerRelationship(**relationship))
                FundManagerRelationship.objects.bulk_create(relationship_objs)
                working_time = self.to_int(manager[6])
                current_fund_best_profit = self.to_float(
                    manager[7]) if manager[7] else 0
                total_asset_manage_amount = self.to_float(
                    manager[10]) if manager[10] else 0
                defaults['name'] = name[0] if name[0] else ''
                defaults['company_id'] = company_id[0] if company_id[0] else ''
                defaults['working_time'] = working_time
                defaults['current_fund_best_profit'] = current_fund_best_profit
                defaults['total_asset_manage_amount'] = total_asset_manage_amount
                exist_manager = FundManager.objects.filter(
                    **{'manager_id': manager_id})
                if exist_manager:
                    exist_manager.update(**defaults)
                else:
                    defaults.update({'manager_id': manager_id})
                    fund_manager_objs.append(FundManager(**defaults))
            except Exception as e:
                logger.warning("parse fund manager error! {}".format(e))
        FundManager.objects.bulk_create(fund_manager_objs)

    @log("{} 更新基金类型".format(datetime.now()))
    def update_fund_type(self):
        fund_types = {'pg': '偏股型', 'gp': '股票型', 'hh': '混合型',
                      'zq': '债券型', 'zs': '指数型', 'qdii': 'QDII', 'fof': 'FOF'}
        for fund_type, type_name in fund_types.items():
            request_url = self.nodejs_server_url + \
                          'fund_type' + '&fund_type={}'.format(fund_type)
            response = self.get(request_url)
            if not response.json()['datas']:
                continue
            funds = response.json()['datas']
            for fund in funds:
                try:
                    fund = fund.split('|')
                    fund_code = fund[0] if fund[0] else ''
                    initial_purchase_amount = self.to_float(
                        fund[-5]) if fund[-5] else ''
                    Fund.objects.filter(fund_code=fund_code).update(
                        **{'fund_type': type_name,
                           'update_time': datetime.now(),
                           'initial_purchase_amount': initial_purchase_amount})
                except Exception as e:
                    logger.warning("update fund type error!  {}".format(e))

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
                val = val.replace('%', '').replace(
                    '---', '').replace('亿元', '').replace('元', '')
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
                return datetime.strptime(val, '%Y-%m-%d')
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

    def get(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            return response
        except Exception as e:
            logger.warning("network error! {}".format(e))
            return {}
