import os
import threading

threading.currentThread()


def sqr(val):
    import time
    time.sleep(0.1)
    print("thread {} result {} current_thread {}".format(os.getpid(), val * val, threading.currentThread().name))
    return val * val


def process_result(result):
    print(result)


def process_these_asap(tasks):
    import concurrent.futures

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        for task in tasks:
            futures.append(executor.submit(sqr, task))

        for future in concurrent.futures.as_completed(futures):
            process_result(future.result())
        # Or instead of all this just do:
        # results = executor.map(sqr, tasks)
        # list(map(process_result, results))


def main():
    tasks = list(range(10))
    print('Processing {} tasks'.format(len(tasks)))
    process_these_asap(tasks)
    print('Done')
    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main())
