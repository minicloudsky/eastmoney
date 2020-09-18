import datetime
import json
import random
import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome


class EasyMoney:
    fundrank_url = 'http://fund.eastmoney.com/data/fundranking.html'
    driver = Chrome()
    year = datetime.datetime.now().year
    funds = []

    def __init__(self):
        self.get_cookie(self.fundrank_url)

    def get_cookie(self, url):
        self.driver.get(url)
        next_btn_xpath = self.element_is_exist()
        self.parse_html(self.driver.page_source)
        while next_btn_xpath:
            self.driver.find_element_by_xpath(next_btn_xpath).click()
            time.sleep(random.randint(4, 10))
            self.parse_html(self.driver.page_source)
            next_btn_xpath = self.element_is_exist()
        with open("D:\\funds.json") as f:
            f.write(json.dumps({'fund': self.funds}))
            f.close()

    def element_is_exist(self):
        next_btn_xpath = '//*[@id="pagebar"]/label[8]'
        backup_next_btn_xpath = '//*[@id="pagebar"]/label[9]'
        try:
            element = self.driver.find_element_by_xpath(next_btn_xpath)
            if element and element.text == '下一页':
                return next_btn_xpath
            else:
                element = self.driver.find_element_by_xpath(backup_next_btn_xpath)
                if element and element.text == '下一页':
                    return backup_next_btn_xpath
            return None
        except Exception as e:
            print("exception! {}".format(e))
            return None

    def to_int(self, val):
        try:
            if val:
                val = val.replace('%', '').replace('---', '')
                val = int(val)
                return val
            return -1
        except Exception as e:
            val = -1
        return val

    def to_float(self, val):
        try:
            if val:
                val = val.replace('%', '').replace('---', '')
                val = float(val)
                return val
            return -1
        except Exception as e:
            val = -1
        return val

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all(id='dbtable')
        table = table[0] if table else ''
        table = table.tbody if table else ''
        trs = list(table.children) if table else []
        for tr in trs:
            fund = {}
            tds = list(tr.children)
            fund['fund_url'] = tds[2].a.attrs['href']
            fund['fund_code'] = tds[2].a.string
            fund['fund_name'] = tds[3].a.attrs['title'] if tds[3].a.attrs['title'] else ''
            fund['fund_shot_name'] = tds[3].a.string if tds[3].a.string else ''
            fund['update_date'] = str(self.year) + "-" + tds[4].string if tds[4] else ''
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
            self.funds.append(fund)


if __name__ == '__main__':
    easymoney = EasyMoney()
