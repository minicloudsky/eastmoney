from django.db import models


# Create your models here.
# 基金
class Fund(models.Model):
    fund_code = models.CharField('基金代码', default='', unique=True, max_length=20, db_index=True)
    fund_name = models.CharField('基金名称', max_length=200, default='')
    fund_type = models.CharField('基金类型', max_length=200, default='')
    fund_short_name = models.CharField('基金简称', max_length=200, default='')
    pinyin_abbreviation_code = models.CharField('基金首字母缩写', max_length=200, default='')
    establish_date = models.DateField('基金创立日期', default='', null=True)
    handling_fee = models.FloatField('手续费率', default=0)
    can_buy = models.BooleanField('可否购买', default=False)
    initial_purchase_amount = models.FloatField('起购金额', default=0)
    currency = models.CharField('货币', default='人民币', max_length=20, null=True, blank=True)
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    def get_fund_url(self):
        return 'http://fund.eastmoney.com/{}.html'.format(self.fund_code)

    def __str__(self):
        return self.fund_code + "_" + self.fund_name


# 基金历史净值排名数据
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
    last_five_year = models.FloatField('最近五年涨跌', default=0)
    ten_thousand_income = models.FloatField('万份收益', default=0)
    annualized_income_7day = models.FloatField('7天年化收益率', default=0)
    annualized_income_14day = models.FloatField('14天年化收益率', default=0)
    annualized_income_28day = models.FloatField('28天年化收益率', default=0)
    this_year = models.FloatField('今年以来涨跌', default=0)
    since_founded = models.FloatField('成立以来涨跌', default=0)
    since_founded_bonus = models.FloatField('成立以来分红', default=0)
    since_founded_bonus_num = models.IntegerField('成立以来分红次数', default=0)
    handling_fee = models.FloatField('手续费率', default=0)
    subscription_status = models.CharField('申购状态', max_length=20, default='', null=True)
    redemption_status = models.CharField('赎回状态', max_length=20, default='', null=True)
    dividend_distribution = models.CharField('分红送配', max_length=200, default='', null=True)
    current_date = models.DateField('当前日期', default='')
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    def __str__(self):
        return self.fund_code + "_" + str(self.current_date)

    class Meta:
        # 添加唯一索引约束，防止每天同一个基金被爬取多次
        unique_together = ('fund_code', 'current_date')


# 基金公司
class FundCompany(models.Model):
    company_id = models.CharField('基金公司 id', max_length=30, unique=True)
    company_name = models.CharField('基金公司名', default='', max_length=100)
    company_short_name = models.CharField('基金公司简称', default='', max_length=30)
    general_manager = models.CharField('总经理', default='', max_length=30)
    establish_date = models.DateField('基金公司创立日期', default='')
    total_manage_amount = models.FloatField('基金管理规模(亿元)', default=0)
    total_fund_num = models.IntegerField('全部基金数', default=0)
    total_manager_num = models.IntegerField('全部基金经理数', default=0)
    tianxiang_star = models.PositiveIntegerField('天相评级', default=0)
    pinyin_abbreviation_code = models.CharField('基金公司首字母缩写', max_length=200, default='')
    update_date = models.DateField('数据更新时间', null=True)
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    def get_fund_company_url(self):
        return 'http://fund.eastmoney.com/company/{}.html'.format(self.company_id)


# 基金经理
class FundManager(models.Model):
    name = models.CharField('基金经理', default='', max_length=20)
    manager_id = models.CharField('基金经理 id', unique=True, max_length=20)
    company_id = models.CharField('所属公司 id', default='', max_length=20)
    working_time = models.IntegerField('从业时间', default=0)
    total_asset_manage_amount = models.FloatField('基金资产管理总规模', default=0)
    current_fund_best_profit = models.FloatField('现任基金最佳回报', default=0)
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    def get_fund_manager_url(self):
        return 'http://fund.eastmoney.com/manager/{}.html'.format(self.manager_id)


# 基金与基金经理关系，多对多中间表
class FundManagerRelationship(models.Model):
    fund_code = models.CharField('基金代码', default='', max_length=20)
    manager_id = models.CharField('基金经理 id', max_length=20)
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', null=True)
    is_deleted = models.IntegerField('是否删除', default=0)

    class Meta:
        unique_together = ('fund_code', 'manager_id')


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
