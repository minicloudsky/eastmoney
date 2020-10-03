#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os

import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eastmoneyspider.settings')
    django.setup()
    from crawler.EastMoneyFundCrawler import EastMoneyFund
    eastmoneyfund = EastMoneyFund()


if __name__ == '__main__':
    main()
