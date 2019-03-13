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
        a,b=self.args
        self.func(a,b)

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
        uploading_files.put_nowait(start_num)
        time.sleep(1)
# 模拟上传文件
def upload_to_server(*args):
    while not exit_flag:
        if uploading_files.not_empty:
            upload_file=uploading_files.get(False)
            print(f"is uploading files:{upload_file}")
        else:
            print('no file to upload')
        time.sleep(1)
uploading_files=queue.Queue(100)
exit_flag=False
thread_lock=threading.Lock()
mythread1=mythread('1',count,0,1)
mythread2=mythread('2',upload_to_server)
mythread1.start()
mythread2.start()

n=0
while n<10:
    time.sleep(1)
    n+=1
    print(f"main thread:{n}")
    if n==9:
        mythread1.exit_flag=True
        mythread2.exit_flag=True

mythread1.join()
mythread2.join()