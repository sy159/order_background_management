import threading,time


def test(x):
    global num
    num+=1
    time.sleep(2)
num = 0
t_obj = []
st = time.time()
for i in range(1000):
    t = threading.Thread(target=test, args=(i,))
    # t.setDaemon(True)
    t.start()
    t_obj.append(t)
for i in t_obj:
    i.join()

# print('main tread is finish...', time.time()-st)
print(num)

# 协程
import gevent
from gevent import monkey
monkey.patch_all()


def test1(url):
    print('test1..')
    time.sleep(2)
    print('test1 agein...')


def test2():
    print('test2 ....')
    time.sleep(1)
    print('test2 agein...')

gevent.joinall([
    gevent.spawn(test1),
    gevent.spawn(test2),
])