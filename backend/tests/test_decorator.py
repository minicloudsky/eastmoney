def deco_para(parameter):
    print('enter deco_para')

    def deco_func(func):
        print('enter deco_func')

        def wrapper(*args, **kwargs):
            print('enter wrapper')
            print(parameter)
            print('---wrapper: before func---')
            func(*args, **kwargs)
            print('---wrapper: after func---')

        return wrapper

    return deco_func


@deco_para(123)
def foo():
    print('---foo---')


if __name__ == '__main__':
    print('--start--')
    # foo()
