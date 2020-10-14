from django.contrib import admin

# Register your models here.
from apps.Fund.models import Fund, FundHistoricalNetWorthRanking, FundCompany, FundManager, FundManagerRelationship, \
    FundLog, FundTask


@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ['id', 'fund_code', 'fund_name', 'fund_type', 'fund_short_name',
                    'pinyin_abbreviation_code', 'establish_date', 'handling_fee',
                    'can_buy', 'currency', 'insert_time', 'update_time',
                    'is_deleted', 'initial_purchase_amount', ]
    list_filter = ['fund_code', 'fund_name', 'fund_type', 'fund_short_name',
                   'pinyin_abbreviation_code', ]
    search_fields = ['fund_code', 'fund_name', 'fund_type', 'fund_short_name',
                     'pinyin_abbreviation_code', ]


@admin.register(FundHistoricalNetWorthRanking)
class FundHistoricalNetWorthRanking(admin.ModelAdmin):
    list_display = ['id', 'fund_code', 'start_unit_net_worth',
                    'start_cumulative_net_worth', 'current_unit_net_worth', 'current_cumulative_net_worth',
                    'daily', 'last_week', 'last_month', 'last_three_month', 'last_six_month',
                    'last_year', 'last_two_year', 'last_three_year', 'last_five_year', 'ten_thousand_income',
                    'annualized_income_7day', 'annualized_income_14day', 'annualized_income_28day',
                    'this_year', 'since_founded', 'since_founded_bonus',
                    'since_founded_bonus_num', 'handling_fee', 'subscription_status',
                    'redemption_status', 'dividend_distribution', 'current_date', 'insert_time',
                    'update_time', 'is_deleted', ]
    list_filter = ['fund_code', 'current_date', 'insert_time',
                   'update_time', ]
    search_fields = ['fund_code', ]


@admin.register(FundCompany)
class FundCompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_id', 'company_name', 'company_short_name',
                    'general_manager', 'establish_date',
                    'total_manage_amount', 'total_fund_num', 'total_manager_num',
                    'tianxiang_star', 'pinyin_abbreviation_code', 'update_date',
                    'insert_time', 'update_time', 'is_deleted', ]
    list_filter = ['company_name', 'company_short_name', 'general_manager', ]
    search_fields = ['company_name', 'company_short_name', 'general_manager', ]


@admin.register(FundManager)
class FundManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'manager_id', 'company_id',
                    'working_time', 'total_asset_manage_amount', 'current_fund_best_profit',
                    'insert_time', 'update_time', 'is_deleted', ]
    list_filter = ['name', ]
    search_fields = ['name', ]


@admin.register(FundManagerRelationship)
class FundManagerRelationshipAdmin(admin.ModelAdmin):
    list_display = ['id', 'fund_code', 'manager_id', 'insert_time', 'update_time',
                    'is_deleted', ]
    list_filter = ['fund_code', 'manager_id', ]
    search_fields = ['fund_code', 'manager_id', ]


@admin.register(FundLog)
class FundLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'total_fund', 'stock_fund_num', 'hybrid_fund_num',
                    'bond_fund_num', 'index_fund_num', 'break_even_fund_num',
                    'qdii_fund_num', 'etf_fund_num', 'lof_fund_num',
                    'fof_fund_num', 'start_time', 'end_time', ]
    list_filter = ['name']
    search_fields = ['name']


@admin.register(FundTask)
class FundLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'func', 'insert_time', 'update_time']
    list_filter = ['func']
    search_fields = ['name', 'func']
