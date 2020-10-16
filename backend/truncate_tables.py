#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os

import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eastmoneyspider.settings')
    django.setup()
    from django.db import connection
    cursor = connection.cursor()
    tables = ['Fund_fund', 'Fund_fundcompany', 'Fund_fundlog',
              'Fund_fundhistoricalnetworth', 'Fund_fundmanager', 'Fund_fundranking',
              'Fund_fundmanagerrelationship', 'Fund_fundtask']
    for table in tables:
        cursor.execute("truncate {}".format(table))
        connection.commit()
    print("truncated tables .")

if __name__ == '__main__':
    main()
