'''
concurrent线程池
为什么要使用线程池？
    1、不仅仅可以提供对线程数量的控制（semaphore的功能）
    2、主线程可以获取某一个线程的状态或者某一个任务的状态，以及返回值
    3、当一个线程完成的时候，我们主线程能立即知道
    4、futures可以让多进程和多线程的编码接口一致

'''
from asyncio import all_tasks
from concurrent import futures  #futures这个包专门用于线程池和进程池编程的：使得编写多进程和多线程的代码异常容易
import time
from concurrent.futures import ThreadPoolExecutor,as_completed,wait,ALL_COMPLETED,FIRST_COMPLETED
from multiprocessing import Process


def get_html(times):
    time.sleep(times)
    print('get page {} success.'.format(times))
    return times

executor = ThreadPoolExecutor(max_workers=2) #max_workers用来指定线程池中的最大工作任务数
#submit是立刻执行并返回结果的
task1 = executor.submit(get_html, 3)
task2 = executor.submit(get_html, 2)

#因为submit是立刻执行并返回结果的，所以task1.done()，返回False
print(task1.done())
#cancel只有在任务还没有开启的时候可以取消成功，在线程池中或者正在执行的时候都无法取消
#可以把线程池的max_workers，改为1，max_workers=1，这样可以取消task2
print(task2.cancel())
#因为submit是立刻执行并返回结果的，所以等待四秒后，task1.done()，返回True
time.sleep(4)
print(task1.done())
#result可以获取执行的结果
print(task1.result())

urls = [3, 2, 4]
'''
as_completed:获取已经成功的task的返回
            哪个任务先结束了，就会返回对应的返回值
'''
all_tasks = [executor.submit(get_html, url) for url in urls]

'''wait用于返回任务处于某种状态下返回对应的返回值'''
wait(all_tasks, return_when=FIRST_COMPLETED)
print('main')
for future in as_completed(all_tasks):
    data = future.result()
    print('page {} done.'.format(data))

'''
executor.map:获取已经完成的task的值
            会按照任务的顺序，执行打印出最后的结果
'''
for data in executor.map(get_html, urls):
    print('page {} done.'.format(data))
'''
future：未来对象，task的返回容器
'''
from concurrent import futures  #futures这个包专门用于线程池和进程池编程的：使得编写多进程和多线程的代码异常容易

'''
多进程编程：耗cpu的操作（多cpu的情况下），用多进程编程；对于io操作来说，用多线程编程
        进程切换操作的代价要高于线程，多数情况下推荐使用多线程编程
        1、对于耗费cpu的操作，多进程要优于多线程
        2、对于io操作来说，多线程优于有多进程
'''
'''计算斐波拉契函数，用线程池'''
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

with ThreadPoolExecutor(3) as executor:
    all_tasks = [executor.submit(fib, num) for num in range(25,40)]
    start_time = time.time()
    for future in as_completed(all_tasks):
        data = future.result()
        print('exec result:{}.'.format(data))
    print('exec time:{}'.format(time.time() - start_time))

'''计算斐波拉契函数，用进程池'''
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

if __name__ == '__main__':

    with ProcessPoolExecutor(3) as executor:
        all_tasks = [executor.submit(fib, num) for num in range(25,40)]
        start_time = time.time()
        for future in as_completed(all_tasks):
            data = future.result()
            print('exec result:{}.'.format(data))
        print('exec time:{}'.format(time.time() - start_time))
'''
多进程编程：进程间的数据是隔离的，无法通过共享变量的形式进行通信
        主进程的结束，不会影响子进程的执行，（但是可能子进程会无法正常退出）
'''
from concurrent.futures import ProcessPoolExecutor #推荐使用
import multiprocessing #更底层的包，便于更好的了解ProcessPoolExecutor
def get_html(times):
    time.sleep(times)
    print('get page {} success.'.format(times))
    return times

if __name__ == '__main__':
    #获取cpu的个数，开启相应的进程数
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    #执行异步操作
    # result = pool.apply_async(get_html, (3,))
    # #必须先关闭
    # pool.close()
    # #等待所有的任务完成
    # pool.join()
    # print(result.get())

#imap方法：执行的结果按照参数的顺序展示
    for result in pool.imap(get_html, [1, 5, 3]):
        print(result)

#imap.unorder方法：执行的结果按照参数谁先执行完谁先输出#
    for result in pool.imap_unordered(get_html, [1, 5, 3]):
        print(result)

'''
进程间通信：
    1、queue：
        有三种queue：
            1、from queue import Queue #只能在线程中使用
            2、from multiprocessing.queues import Queue
            3、from multiprocessing import Manager
               Manager().Queue()
    2、pipe：只能用于两个进程，但是效率高于queue
    3、manager
'''
from multiprocessing import Process, Queue
# from queue import Queue
import time
def procesor(queue):
    queue.put('a')
    time.sleep(2)

def customer(queue):
    time.sleep(2)
    data = queue.get()
    print(data)

if __name__ == '__main__':
    queue = Queue(10)
    procesor_process = Process(target=procesor, args=(queue,))
    customer_process = Process(target=customer, args=(queue,))
    procesor_process.start()
    customer_process.start()
    procesor_process.join()
    customer_process.join()

'''共享全局变量不适用于多进程通信'''
from multiprocessing import Process, Queue
import multiprocessing
# from queue import Queue
import time
def procesor(a):
    a +=100
    time.sleep(2)

def customer(a):
    time.sleep(2)
    print(a)

if __name__ == '__main__':
    a = 1
    procesor_process = Process(target=procesor, args=(a,))
    customer_process = Process(target=customer, args=(a,))
    procesor_process.start()
    customer_process.start()
    procesor_process.join()
    customer_process.join()

'''multiprocessing中的queue，不能用于进程池中的通信'''
from multiprocessing import Pool, Queue
# from queue import Queue
import time
def procesor(queue):
    queue.put('a')
    time.sleep(2)

def customer(queue):
    time.sleep(2)
    data = queue.get()
    print(data)

if __name__ == '__main__':
    queue = Queue(10)
    pool = Pool(processes=2)
    pool.apply_async(procesor, args=(queue,))
    pool.apply_async(customer, args=(queue,))
    pool.close()
    pool.join()

'''multiprocessing中的queue，不能用于进程池中的通信
    但是可以用Manager中的queue
'''
from multiprocessing import Pool, Queue
from multiprocessing import Manager
import time
def procesor(queue):
    queue.put('a')
    time.sleep(2)

def customer(queue):
    time.sleep(2)
    data = queue.get()
    print(data)

if __name__ == '__main__':
    #
    queue = Manager().Queue()
    pool = Pool(processes=2)
    pool.apply_async(procesor, args=(queue,))
    pool.apply_async(customer, args=(queue,))
    pool.close()
    pool.join()
'''
 通过pipe实现进程间通信
'''
from multiprocessing import Process, Pipe
import time
def procesor(pipe):
    pipe.send(1)

def customer(pipe):
    print(pipe.recv())

if __name__ == '__main__':
    #pipe只能用于两个进程间通信
    receive_pipe, send_pipe = Pipe()
    my_procesor = Process(target=procesor, args=(send_pipe,))
    my_customer = Process(target=customer, args=(receive_pipe,))
    my_procesor.start()
    my_customer.start()
    my_procesor.join()
    my_customer.join()

'''
 通过Manager实现进程间共享内存操作
'''
from multiprocessing import Process, Manager
import time
def add_data(pro_dict,key, value):
    pro_dict[key] = value
    print(pro_dict)

if __name__ == '__main__':
    process_dict = Manager().dict()
    first_procesor = Process(target=add_data, args=(process_dict, 'leaya', 1))
    second_processor = Process(target=add_data, args=(process_dict, 'leaya', 2))
    first_procesor.start()
    second_processor.start()
    first_procesor.join()
    second_processor.join()