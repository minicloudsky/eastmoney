import threading
import time

g_num = 0


def work1(num):
    global g_num
    for i in range(num):
        if mutex.acquire(True):
            g_num += 1
            mutex.release()
    print('---in work1,g_num in %d---' % g_num)


def work2(num):
    global g_num
    for i in range(num):
        if mutex.acquire(True):
            g_num += 1
            mutex.release()
    print('---in work2,g_num in %d---' % g_num)


print('---线程创建之前g_num: %d' % g_num)

mutex = threading.Lock()

t1 = threading.Thread(target=work1, args=(1000000,))
t2 = threading.Thread(target=work2, args=(1000000,))

t1.start()
time.sleep(1)
t2.start()

while len(threading.enumerate()) != 1:
    time.sleep(1)

print('2个线程对同一个变量操作之后的最终结果：%d' % g_num)
