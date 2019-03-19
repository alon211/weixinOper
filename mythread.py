import threading
import time
from scrapy_log import *
import queue
from upload_github import*
PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue()
uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
con=threading.Condition()
print(uploadedfiles)
# 模拟生成新的文件
def product(*args):
    data,exit_flag=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    tmp={}
    if con.acquire():
        while not exit_flag:
            # time.sleep(1)
            if len(tmp)==0:
                print(f'{thread_name}:no new file')
                tmp=get_newlogset(PATH,uploadedfiles)
                con.wait()
                continue
            i=tmp.pop()
            print(f'{thread_name} is putting data on the queue')
            # print(i)
            uploadedfiles.add(i)
            data.put(i)
            print(f'{thread_name} have put data on the queue')
            print(f'{thread_name}- data size :{data.qsize()}')
            con.notify()
            con.wait()
# 模拟上传文件
def consumer(*args):
    data,=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    isuploaded=True
    if con.acquire():
        while True:
            try:

                # lock.acquire()
                value=data.get(timeout=1)
                print(f'{thread_name} get a vaule:{value} in the queue')
                print(f'{thread_name}: uploading to github')
                print(f'{git_oper(value)}')
                save_uploadedfile('uploadedfiles.txt',value)
                # lock.release()
                print(f'{thread_name}- data size :{data.qsize()}')
                con.notify()
                con.wait()
            except :
                print(f'the queue is empty,{thread_name} is waiting a value ')
                con.notify()
                con.wait()

lock=threading.Lock()
exit_flag=False
thread_lock=threading.Lock()
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_prodcut.start()
thread_consumer.start()
thread_prodcut.join()
thread_consumer.join()