import threading
import time
from scrapy_log import *
import queue
PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue()
uploadedfiles=set()
# 模拟生成新的文件
def product(*args):
    data,exit_flag=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    while not exit_flag:
        time.sleep(1)
        tmp=get_newlogset(PATH,uploadedfiles)
        if tmp=={}:
            print('{thread_name}:no new file')
            continue
        for i in tmp:
            print(f'{thread_name} is putting data on the queue')
            data.put(i)
        print(f'{thread_name} have put data on the queue')
        print(f'{thread_name}- data size :{data.qsize()}')
# 模拟上传文件
def consumer(*args):
    data,=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    while True:
        try:
            value=data.get()
            uploadedfiles.add(value)
            print(f'{thread_name} get a vaule:{value} in the queue')
            print(f'{thread_name}- data size :{data.qsize()}')
        except :
            print(f'the queue is empty,{thread_name} is waiting a value ')


uploading_files=queue.Queue(100)
exit_flag=False
thread_lock=threading.Lock()
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_prodcut.start()
thread_consumer.start()

thread_prodcut.join()
thread_consumer.join()