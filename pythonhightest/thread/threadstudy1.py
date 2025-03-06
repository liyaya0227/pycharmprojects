'''
GIL：global interpreter lock
gil使得同一个时刻只有一个线程在cpu上执行字节码，无法将多个线程映射到多个cpu上执行
但是gil会根据执行的字节码行数以及时间片释放gil，gil在遇到io操作时主动释放
'''
import queue
import threading
import time

'''
thread
对于io操作来说，多线程和多进程的差别不大
'''
'''
1、thread
'''
# def get_detail_html():
#     print("get_detail_html start")
#     time.sleep(2)
#     print("get_detail_html end")
#
# def get_detail_url():
#     print("get_detail_url start")
#     time.sleep(4)
#     print("get_detail_url end")

# if __name__ == '__main__':
#     thread1 = threading.Thread(target=get_detail_html, args=('',))#参数args是元组类型
#     thread2 = threading.Thread(target=get_detail_url, args=('',))
#     start_time = time.time()
#     #将子线程设置为了守护线程。根据setDaemon()方法的含义，父线程打印内容后便结束了，不管子线程是否执行完毕了
#     thread1.setDaemon(True)
#     thread1.start()
#     thread2.start()
#     #jion()确保子线程能执行完毕，才开始往下执行
#     thread1.join()
#     thread2.join()
#     print("last_time:{}".format(time.time()-start_time()))

'''
2、通过继承Thread来实现多线程
'''
class Get_Detail_Html(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("get_detail_html start")
        time.sleep(2)
        print("get_detail_html end")


class Get_Detail_Url(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("get_detail_url start")
        time.sleep(4)
        print("get_detail_url end")

if __name__ == '__main__':
    thread1 = Get_Detail_Html("get_detail_html")
    thread2 = Get_Detail_Url("get_detail_url")
    start_time = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print("last_time:{}".format(time.time() - start_time))

'''
3、线程间的通信方式：1、共享变量：不安全，不推荐，因为gil会根据执行的字节码行数以及时间片释放gil，gil在遇到io操作时主动释放
                2、queue
'''
url_list = []
def get_detail_html(url_list):

    while True:
        if len(url_list) == 0:
            url = url_list.pop()
            print("get_detail_html start")
            time.sleep(2)
            print("get_detail_html end")

def get_detail_url(url_list):
    print("get_detail_url start")
    while True:
        for i in range(20):
            url_list.append("https://www.baidu.com/{id}".format(id=i))
        time.sleep(4)
        print("get_detail_url end")

if __name__ == '__main__':
    thread1 = threading.Thread(target=get_detail_html, args=('url_list',))#参数args是元组类型
    for i in range(10):
        thread2 = threading.Thread(target=get_detail_url, args=('url_list',))
        thread2.start()
    start_time = time.time()
    #将子线程设置为了守护线程。根据setDaemon()方法的含义，父线程打印内容后便结束了，不管子线程是否执行完毕了
    thread1.setDaemon(True)
    thread1.start()
'''
2、queue
'''
from queue import Queue
url_list = []
def get_detail_html(queue):

    while True:
        url = queue.get()
        print("get_detail_html start")
        time.sleep(2)
        print("get_detail_html end")

def get_detail_url(queue):
    while True:
        print("get_detail_url start")
        for i in range(20):
            queue.put("https://www.baidu.com/{id}".format(id=i))
        time.sleep(4)
        print("get_detail_url end")

if __name__ == '__main__':
    detail_url_queue = Queue(maxsize=1000)
    thread1 = threading.Thread(target=get_detail_html, args=('detail_url_queue',))#参数args是元组类型
    for i in range(10):
        html_thread = threading.Thread(target=get_detail_url, args=('detail_url_queue',))
        html_thread.start()
    start_time = time.time()
    #将子线程设置为了守护线程。根据setDaemon()方法的含义，父线程打印内容后便结束了，不管子线程是否执行完毕了
    thread1.setDaemon(True)
    thread1.start()
    detail_url_queue.task_done() #  确保queue能正确退出
    detail_url_queue.join()

'''
4、线程同步：lock、rlock、condition、semaphore
        1、lock：容易造成死锁
        2、rlock：解决死锁问题，但是每次必须释放
        3、condition：用于复杂线程中同步锁，条件变量
        4、semaphore：用于控制进入数量的锁
'''
'''
1、lock：获取、释放锁，都很浪费时间，会影响性能；还会造成死锁
'''
# from  threading import Lock
# lock = Lock()
# #获取锁
# lock.acquire()
# #释放锁
# lock.release()
'''
2、rlock(可重入的锁)：在同一个线程中，可以连续调用多次acquire，但是要注意acquire和release的次数一定要一样多
'''
# from  threading import RLock
# lock = RLock()
# lock.acquire()
# lock.release()
# lock.acquire()
# lock.release()
'''
3、condition：用于复杂线程中同步锁，条件变量
    例如：天猫精灵和小爱同学互相对话，你一言我一语  
'''
from threading import Condition
condition = Condition(lock)
import threading
'''只用lock无法完成协同工作：会出现一个程序执行完之后，才会执行下一个程序的内容'''
class TianMao():
    def __init__(self, name,lock):
        super().__init__()
        self.name = name
        self.lock = lock

    def run(self):
        print('{}: 小爱同学'.format(self.name))
        lock.acquire()
        print('{}: 我们来诗词接龙吧'.format(self.name))
        lock.release()

class XiaoAi():
    def __init__(self, name, lock):
        super().__init__()
        self.name = name
        self.lock = lock

    def run(self):
        print('{}：在'.format(self.name))
        lock.acquire()
        print('{}: 好啊'.format(self.name))
        lock.release()

if __name__ == '__main__':
    lock = threading.RLock()
    tianmao = TianMao('天猫精灵',lock)
    xiaoai = XiaoAi('小爱同学',lock)

    tianmao.start()
    xiaoai.start()

'''优化：使用condition'''
from threading import Condition

class TianMao(threading.Thread):
    def __init__(self, cond):
        super().__init__(name= '天猫精灵')
        self.cond = cond

    def run(self):
        with self.cond:
            print('{}: 小爱同学'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            print('{}: 我们来诗词接龙吧'.format(self.name))
            self.cond.notify()
            self.cond.wait()

class XiaoAi(threading.Thread):
    def __init__(self, cond):
        super().__init__(name= '小爱同学')
        self.cond = cond

    def run(self):
        with self.cond:
            self.cond.wait()
            print('{}：在'.format(self.name))
            self.cond.notify()
            self.cond.wait()
            print('{}: 好啊'.format(self.name))
            self.cond.notify()
            # self.cond.wait()



if __name__ == '__main__':
    cond = threading.Condition()
    tianmao = TianMao(cond)
    xiaoai = XiaoAi(cond)
    #启动顺序很重要
    #只有在with sef.cond 之后才能调用wait和notify方法
    #condition有两把锁，底层的锁会在调用wait方法的时候释放，上面的锁会在每次调用wait方法的时候分配一把并放入cond的等待队列中//
    #等待notify的唤醒
    xiaoai.start()
    tianmao.start()


'''
4、semaphore：用于控制进入数量的锁
        文件的读写操作，写一般只允许一个线程操作，而读可以多个线程同时操作
'''
from threading import Semaphore

class Html_Thread(threading.Thread):
    def __init__(self, url, sem):
        super().__init__()
        self.url = url
        self.sem = sem

    def run(self):
        time.sleep(2)
        print("producer start")
        #在执行的线程里面释放
        self.sem.release()


class UrlProducer(threading.Thread):
    def __init__(self, sem):
        super().__init__()
        self.sem = sem

    def run(self):
        for i in range(20):
            self.sem.acquire()
            html_thread = Html_Thread("http://www.baidu.com/{id}".format(id = i), self.sem)
            html_thread.start()


if __name__ == '__main__':
    #控制每次同时运行的线程数为3
    sem = threading.Semaphore(3)
    url_producer = UrlProducer(sem)
    url_producer.start()
