from django.db import models


# Create your models here.
class Fund(models.Model):
    fund_code = models.CharField('基金代码', default='', unique=True, max_length=20, db_index=True)
    fund_name = models.CharField('基金名称', max_length=200, default='')
    fund_manager = models.CharField('基金经理', max_length=200, default='')
    fund_company = models.CharField('基金公司', max_length=200, default='')
    fund_type = models.CharField('基金类型', max_length=200, default='')
    fund_short_name = models.CharField('基金简称', max_length=200, default='')
    pinyin_abbreviation_code = models.CharField('基金首字母缩写', max_length=200, default='')
    establish_date = models.DateField('基金创立日期', default='')
    handling_fee = models.FloatField('手续费率', default=0)
    can_buy = models.BooleanField('可否购买', default=False)
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    def get_fund_url(self):
        return 'http://fund.eastmoney.com/{}.html'.format(self.fund_code)

    def __str__(self):
        return self.fund_code + "_" + self.fund_name


class FundHistoricalNetWorthRanking(models.Model):
    fund_code = models.CharField('基金代码', default='', max_length=20, db_index=True)
    start_unit_net_worth = models.FloatField('起始单位净值', default=0)
    start_cumulative_net_worth = models.FloatField('起始累计净值', default=0)
    current_unit_net_worth = models.FloatField('当前单位净值', default=0)
    current_cumulative_net_worth = models.FloatField('当前累计净值', default=0)
    daily = models.FloatField('日涨跌幅', default=0)
    last_week = models.FloatField('周涨跌', default=0)
    last_month = models.FloatField('最近一个月涨跌', default=0)
    last_three_month = models.FloatField('最近三个月涨跌', default=0)
    last_six_month = models.FloatField('最近六个月涨跌', default=0)
    last_year = models.FloatField('最近一年涨跌', default=0)
    last_two_year = models.FloatField('最近两年涨跌', default=0)
    last_three_year = models.FloatField('最近三年涨跌', default=0)
    this_year = models.FloatField('今年以来涨跌', default=0)
    since_founded = models.FloatField('成立以来涨跌', default=0)
    since_founded_bonus = models.FloatField('成立以来分红', default=0)
    since_founded_bonus_num = models.IntegerField('成立以来分红次数', default=0)
    handling_fee = models.FloatField('手续费率', default=0)
    subscription_status = models.CharField('申购状态', max_length=20, default='')
    redemption_status = models.CharField('赎回状态', max_length=20, default='')
    dividend_distribution = models.CharField('分红送配', max_length=200, default='')
    current_date = models.DateField('当前日期', default='')
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    def __str__(self):
        return self.fund_code + "_" + str(self.current_date)

    class Meta:
        # 添加唯一索引约束，防止每天同一个基金被爬取多次
        unique_together = ('fund_code', 'current_date')


# 基金爬取日志
class FundLog(models.Model):
    name = models.CharField('爬取名称', max_length=100, default='')
    total_fund = models.PositiveIntegerField('基金总数', default=0)
    stock_fund_num = models.PositiveIntegerField('股票型基金总数', default=0)
    hybrid_fund_num = models.PositiveIntegerField('混合型基金总数', default=0)
    bond_fund_num = models.PositiveIntegerField('债券型基金总数', default=0)
    index_fund_num = models.PositiveIntegerField('指数基金总数', default=0)
    break_even_fund_num = models.PositiveIntegerField('保本型基金总数', default=0)
    qdii_fund_num = models.PositiveIntegerField('QDII 型基金总数', default=0)
    etf_fund_num = models.PositiveIntegerField('ETF 型基金总数', default=0)
    lof_fund_num = models.PositiveIntegerField('LOF型基金总数', default=0)
    fof_fund_num = models.PositiveIntegerField('FOF型基金总数', default=0)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')

    def __str__(self):
        return self.name
