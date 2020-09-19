from django.db import models


# Create your models here.


class Fund(models.Model):
    fund_url = models.CharField('基金链接', max_length=300, default='')
    fund_code = models.CharField('基金代码', default='', max_length=20)
    fund_name = models.CharField('基金名称', max_length=200, default='')
    fund_short_name = models.CharField('基金简称', max_length=200, default='')
    update_date = models.DateField('当前日期')
    unit_net_worth = models.FloatField('单位净值', default=0)
    cumulative_net_worth = models.FloatField('累计净值', default=0)
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
    handling_fee = models.FloatField('手续费率', default=0)
    is_deleted = models.IntegerField('是否删除', default=0)
    insert_time = models.DateTimeField('爬取时间', auto_now_add=True)

    def __str__(self):
        return self.fund_name

    class Meta:
        # 添加唯一索引约束，防止每天同一个基金被爬取多次
        unique_together = ('fund_url', 'fund_code', 'fund_name', 'update_date')


class FundLog(models.Model):
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    total_fund = models.PositiveIntegerField('基金总数', default=0)
