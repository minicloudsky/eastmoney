import datetime
import logging
import math
import random
import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from apps.Fund.models import FundHistoricalNetWorthRanking, FundLog

logger = logging.getLogger("eastmoney")


# 东方财富基金
class EastMoneyFund:
    fundrank_url = 'http://fund.eastmoney.com/data/fundranking.html'
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    driver = Chrome(chrome_options=chrome_options)
    year = datetime.datetime.now().year
    total_funds = 0
    default_max_page = 200

    def __init__(self):
        self.get_fund(self.fundrank_url)

    def get_fund(self, url):
        logger.info("Start crawl easymoney fund .")
        start_time = datetime.datetime.now()
        next_btn_xpath = '//*[@id="pagebar"]/label[8]'
        backup_next_btn_xpath = '//*[@id="pagebar"]/label[9]'
        self.driver.get(url)
        time.sleep(random.randint(9, 15))
        self.parse_html(self.driver.page_source)
        total_page = self.get_total_page()
        for i in range(total_page):
            try:
                element = self.driver.find_element_by_xpath(next_btn_xpath)
                if element and element.text == '下一页':
                    self.driver.find_element_by_xpath(next_btn_xpath).click()
                else:
                    element = self.driver.find_element_by_xpath(backup_next_btn_xpath)
                    if element and element.text == '下一页':
                        self.driver.find_element_by_xpath(backup_next_btn_xpath).click()
            except Exception as e:
                logger.warning("exception! {}".format(e))
            time.sleep(random.randint(9, 15))
            self.parse_html(self.driver.page_source)
        self.driver.close()
        end_time = datetime.datetime.now()
        FundLog.objects.create(start_time=start_time, end_time=end_time, total_fund=self.total_funds)
        logger.info("Crawl eastmoney fund finished .")

    def get_total_page(self):
        element = self.driver.find_element_by_xpath('//*[@id="types"]/li[1]')
        if element:
            logger.info(element.text)
            total = element.text.replace('全部', '').replace('(', '').replace(')', '').replace(' ', '')
            page = math.ceil(int(total) / 50) if total else 200
            logger.info("total page: {}".format(page))
            return page
        else:
            return self.default_max_page

    def to_int(self, val):
        try:
            if val:
                val = val.replace('%', '').replace('---', '')
                val = int(val)
                return val
            return -9999
        except Exception as e:
            logger.warning("parsing number error! {} - {}".format(val, e))
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
            logger.warning("parsing number error! {} - {}".format(val, e))
            val = -9999
        return val

    # 日期时间转换，将 09-17 转为 2020-09-17
    def format_datetime(self, val):
        try:
            if val:
                val = str(self.year) + "-" + val
                val = datetime.datetime.strptime(val, '%Y-%m-%d')
                return val
            return str(datetime.datetime.now())
        except Exception as e:
            val = str(datetime.datetime.now())
            logger.warning("format date error {}".format(e))
            return val

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all(id='dbtable')
        table = table[0] if table else ''
        table = table.tbody if table else ''
        trs = list(table.children) if table else []
        funds = []
        # tr里面一行是一个基金的详细数据
        for tr in trs:
            fund = {}
            tds = list(tr.children)
            fund['fund_url'] = tds[2].a.attrs['href']
            fund['fund_code'] = tds[2].a.string
            fund['fund_name'] = tds[3].a.attrs['title'] if tds[3].a.attrs['title'] else ''
            fund['fund_short_name'] = tds[3].a.string if tds[3].a.string else ''
            fund['update_date'] = self.format_datetime(tds[4].string)
            fund['unit_net_worth'] = self.to_float(tds[5].string)
            fund['cumulative_net_worth'] = self.to_float(tds[6].string)
            fund['daily'] = self.to_float(tds[7].string)
            fund['last_week'] = self.to_float(tds[8].string)
            fund['last_month'] = self.to_float(tds[9].string)
            fund['last_three_month'] = self.to_float(tds[10].string)
            fund['last_six_month'] = self.to_float(tds[11].string)
            fund['last_year'] = self.to_float(tds[12].string)
            fund['last_two_year'] = self.to_float(tds[13].string)
            fund['last_three_year'] = self.to_float(tds[14].string)
            fund['this_year'] = self.to_float(tds[15].string)
            fund['since_founded'] = self.to_float(tds[16].string)
            fund['handling_fee'] = self.to_float(tds[18].string)
            is_exist = FundHistoricalNetWorthRanking.objects.filter(update_date=fund['update_date'],
                                                                    fund_code=fund['fund_code'],
                                                                    fund_url=fund['fund_url'],
                                                                    fund_name=fund['fund_name']).first()
            if not is_exist:
                funds.append(FundHistoricalNetWorthRanking(**fund))
            else:
                logger.warning(
                    "{}-{}-{} exists!".format(fund['fund_code'], fund['fund_name'], str(fund['update_date'])))
        FundHistoricalNetWorthRanking.objects.bulk_create(funds)
        self.total_funds += len(funds)


if __name__ == '__main__':
    easymoney = EastMoneyFund()
