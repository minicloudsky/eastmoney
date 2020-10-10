import functools
import logging
from datetime import datetime

from apps.Fund.models import FundLog

logger = logging.getLogger("easymoneyfundcrawler")


def log(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.warning('开始执行 %s %s():' % (text, func.__name__))
            FundLog.objects.create(name='开始执行 %s %s():' % (text, func.__name__),
                                   start_time=datetime.now(), end_time=datetime.now())
            func(*args, **kwargs)
            logger.warning('{} {}() 执行完成:'.format(text, func.__name__))
            FundLog.objects.create(name='{} {}() 执行完成:'.format(text, func.__name__),
                                   start_time=datetime.now(), end_time=datetime.now())

        return wrapper

    return decorator
