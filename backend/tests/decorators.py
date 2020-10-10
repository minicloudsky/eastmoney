from datetime import datetime
import functools


# def log(func):
#     def wrapper(*args, **kwargs):
#         print('call %s(): ' % func.__name__)
#         return func(*args, **kwargs)
#
#     return wrapper

def log(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('%s %s(): ' % (text, func.__name__))
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('call %s(): ' % func.__name__)
        return func(*args, **kwargs)

    return wrapper


def log3(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('%s %s():' % (text, func.__name__))
            func(*args, **kwargs)
            print("zzzzzzzzzzzzzzzzzzzzzz")
        return wrapper
    return decorator


@log3("{} 开始执行".format(datetime.now()))
def now():
    print(" i am python")


if __name__ == '__main__':
    now()
