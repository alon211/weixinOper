import threading
import time
from scrapy_log import *
import queue
# class mythread(threading.Thread):
#     def __init__(self,name,func,*args):
#         threading.Thread.__init__(self)
#         self.thread_name=name
#         self.func=func
#         self.args=args
#         self._exit_falg=False
#     def run(self):
#         while not self._exit_flag:
#             print(f'thread {self.name} is running......')
#
#         print(f'thread {self.name} is stopping......')

class mythread(threading.Thread):
    def __init__(self,name,func,*args):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
        self._exit_flag=False
    def run(self):
        if self.name=='count':
            n,=self.args
            self.func(self.name,n)
        else:
            self.func()

    @property
    def exit_flag(self):
        return self._exit_flag
    @exit_flag.setter
    def exit_flag(self,value):
        self._exit_flag=value
# 模拟生成新的文件
def count(threadname,init_num):
    start_num=init_num
    while not exit_flag:
        start_num+=1
        print(f'get a new file:{start_num}')
        uploading_files.put_nowait(start_num)
        time.sleep(1)
# 模拟上传文件
def upload_to_server(*args):
    while not exit_flag:
        if uploading_files.not_empty:
            print(f'queue statuse:{uploading_files.empty()}')
            upload_file=uploading_files.get(False)
            print(f"is uploading files:{upload_file}")
        else:
            print('no file to upload')
        time.sleep(1)
uploading_files=queue.Queue(100)
exit_flag=False
thread_lock=threading.Lock()
mythread1=mythread('count',count,2)
mythread2=mythread('upload_to_server',upload_to_server)
mythread1.start()
mythread2.start()

n=0
while n<10:
    time.sleep(1)
    n+=1
    print(f"main thread:{n}")
    if n==9:
        thread_lock.acquire()
        exit_flag=True
        thread_lock.release()

mythread1.join()
mythread2.join()