import threading
import time
from scrapy_log import *
import queue
from upload_github import*
PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue()
uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
con=threading.Condition()
isEmpty=True
print(uploadedfiles)
# 模拟生成新的文件
def product(*args):
    data,exit_flag=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    uploading_files={}

    while not exit_flag:
        # time.sleep(1)
        con.acquire()
        global uploadedfiles
        if len(uploading_files)==0:
            # lock.acquire()
            print(f'{thread_name}:no new file')
            uploading_files=get_newlogset(PATH,uploadedfiles)
            # print(uploadedfiles)
            # lock.release()
            continue
        # lock.acquire()
        i=uploading_files.pop()
        print(f'{thread_name} is putting data on the queue')
        # print(i)
        uploadedfiles.add(i)
        data.put(i)
        print(f'{thread_name} have put data on the queue')
        print(f'{thread_name}- data size :{data.qsize()}')
        # lock.release()
        global isEmpty
        isEmpty=False
        con.notify()
        con.wait()
# 模拟上传文件
def consumer(*args):
    data,=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    isuploaded=True
    status=None
    while True:
        # lock.acquire()
        try:
            con.acquire()

            global uploadedfiles,isEmpty
            if not isEmpty:
                value=data.get(timeout=1)
            # print(f'value={value}')
            print(f'{thread_name} get a vaule:{value} in the queue')
            # print(f'{thread_name}: uploading to github')
            status=git_oper(value)[0]
            print(f'-------------------status:{status}')
            # 传送失败,重新放入队列
            if not status:
                # lock.acquire()
                print(f'fail to upload {value}')
                # data.put(value)
                uploadedfiles.remove(value)
                con.notify()
                con.wait()
                # lock.release()
                time.sleep(10)
                continue
            # lock.acquire()
            save_uploadedfile('uploadedfiles.txt',value)
            print(f'{thread_name}- data size :{data.qsize()}')
            # lock.release()
            con.notify()
            con.wait()
        except Exception as e:
            isEmpty=True
            print(f'Error:{e}')
            # print(status)
            # print(value)
            print(f'the queue is empty,{thread_name} is waiting a value ')
            # lock.release()
            con.notify()
            con.wait()
        # lock.release()

lock=threading.RLock()
exit_flag=False
thread_lock=threading.Lock()
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_prodcut.start()
thread_consumer.start()
thread_prodcut.join()
thread_consumer.join()