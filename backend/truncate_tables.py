#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os

import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eastmoney.settings')
    django.setup()
    from django.db import connection
    cursor = connection.cursor()
    tables = ['fund_fund', 'fund_fundcompany', 'fund_fundlog',
              'fund_fundhistoricalnetworth', 'fund_fundmanager', 'fund_fundranking',
              'fund_fundmanagerrelationship', 'fund_fundtask']
    for table in tables:
        cursor.execute("truncate {}".format(table))
        connection.commit()
    print("truncated tables .")


if __name__ == '__main__':
    main()
