import threading, time

# #创建event
# event = threading.Event()
#
# #重置代码中的event对象，使得所有该event事件都处于待命状态
# event.clear()
#
# #阻塞线程，等待event指令
# event.wait()
#
# #发送event指令，使得所有设置该event事件的线程执行
# event.set()

#性能测试集合点
class MyThread(threading.Thread):
    def __init__(self, event):
        super().__init__()
        self.event = event

    def run(self):
        print("线程{}初始化完成，随之准备启动".format(self.name))
        #设置线程等待
        self.event.wait()
        print("{}开始执行...".format(self.name))

if __name__ == '__main__':
    event = threading.Event()
    threads = []
    #创建10个自定义线程
    [threads.append(MyThread(event)) for i in range(1,11)]

    event.clear()
    [t.start() for t in threads]
    time.sleep(3)
    event.set()
    [t.join() for t in threads]