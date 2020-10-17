#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import configparser
import os

import django


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eastmoneyspider.settings')
    django.setup()
    config = configparser.ConfigParser()
    config.sections()
    config.read("config.ini")
    print(config['CRAWL_MODE']['crawl_mode'])

if __name__ == '__main__':
    main()
