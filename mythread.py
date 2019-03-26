import threading
import time
from scrapy_log import *
import queue
from upload_github import*
PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue(10)

uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
con=threading.Condition()
isEmpty=True
print(uploadedfiles)
lock1=False
lock2=False
# 模拟生成新的文件
def product(*args):
    data,exit_flag=args
    thread_name=threading.current_thread().name
    print(f'{thread_name}: start!')
    uploadingfiles={}

    while not exit_flag:

        # con.acquire()
        global uploadedfiles,lock1,lock2,isEmpty
        if len(uploadingfiles)==0 and lock1==False:
            # lock.acquire()
            print(f'{thread_name}:no new file')
            uploadingfiles=get_newlogset(PATH,uploadedfiles)
            continue
        if len(uploadingfiles)>0:
            lock1=True
            i=uploadingfiles.pop()
            print(f'{thread_name} is putting data on the queue')
            # print(i)
            # uploadedfiles.add(i)
            print(f'{thread_name}- data size :{data.qsize()}')
            data.put(i)
            isEmpty=False

            print(f'{thread_name} have put data on the queue')

    # lock.release()
        # con.notify()
        # con.wait()
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
            # con.acquire()

            global uploadedfiles,isEmpty,lock1
            # 队列是否为空
            if not isEmpty:
                # lock1=True
                value=data.get(timeout=1)
                uploadedfiles.add(value)
                lock1=False
            # print(f'value={value}')
                print(f'{thread_name} get a vaule:{value} in the queue')
            # print(f'{thread_name}: uploading to github')

                save_uploadedfile('uploadedfiles.txt',value)
                print(f'{thread_name}- data size :{data.qsize()}')

            # con.notify()
            # con.wait()

                t=git_oper(value)
            # con.acquire()
                status=t[0]
                errcode=t[1]
                print(f'-------------------status:{status}')
            # 传送失败,重新放入队列,
            # 其实可以不考虑的，但正常流程操作应该考虑，这是由于git本来的机制你push时就算
            # 断网，之后联网后他也会自动push的
                if not status:
                    # lock.acquire()
                    print(f'fail to upload {value}')
                    print(f'errcode:{errcode}')
                    # github已经上传相同的文件而且没有变化就会报errcode，重复上传
                    if errcode==1:
                        uploadedfiles.add(value)
                        save_uploadedfile('uploadedfiles.txt',value)

                    else:
                        uploadedfiles.remove(value)
                    # con.notify()
                    # con.wait()

                    time.sleep(1)
                    continue

            # save_uploadedfile('uploadedfiles.txt',value)
            # print(f'{thread_name}- data size :{data.qsize()}')

            # con.notify()
            # con.wait()
        except Exception as e:
            print(f'Error:{e}')
            # print(status)
            # print(value)
            print(f'the queue is empty,{thread_name} is waiting a value ')
            isEmpty=True

            # con.notify()
            # con.wait()


lock=threading.RLock()
exit_flag=False
thread_lock=threading.Lock()
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_prodcut.start()
thread_consumer.start()
thread_prodcut.join()
thread_consumer.join()