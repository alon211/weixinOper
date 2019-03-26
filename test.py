# from wxpy import *
# bot=Bot(cache_path=True)
# friend=bot.friends().search(name='张工')[0]
# friend.send('hello')
# embed()
import threading
from time import gmtime
from scrapy_log import *
import queue
from upload_github import*
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s | %(asctime)s.%(msecs)05d   %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=r'C:\Users\admin\PycharmProjects\weixinOper\test.log',
                    filemode='w')
# 模拟生成新的文件
def product(*args):
    data,exit_flag=args
    thread_name=threading.current_thread().name
    logging.info(f'{thread_name}: start!')
    uploadingfiles={}
    while not exit_flag :
        if len(uploadedfiles)!=0:
            logging.info(f'{threading.current_thread().name} will get a value from upladedfiles')
            value=uploadedfiles.pop()
            logging.info(f'{threading.current_thread().name} will put a value')
            data.put(value)
            logging.info(f'{threading.current_thread().name} have put a value {value}')
            logging.info(f'{threading.current_thread().name} : data size  {data.qsize()}')
        else:
            logging.info(f'{threading.current_thread().name} : waiting new file ')
# 模拟上传文件
def consumer(*args):
    data,=args
    thread_name=threading.current_thread().name
    logging.info(f'{thread_name}: start!')
    isuploaded=True
    status=None
    while True:
        # lock.acquire()
        try:
            logging.info(f'{threading.current_thread().name} will get a value')
            value=data.get(timeout=1)
            logging.info(f'{threading.current_thread().name} will push to git -------------')
            git_oper(value)
            logging.info(f'{threading.current_thread().name} have got a value {value}')
        except Exception as e:
            logging.info(f'Error:{e}')
            # print(status)
            # print(value)
            logging.info(f'the queue is empty,{thread_name} is waiting a value ')
            # time.sleep(0.1)
            isEmpty=True

            # con.notify()
            # con.wait()



PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue(10)

uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
con=threading.Condition()
isEmpty=True
print(uploadedfiles)
lock1=False
lock2=False
lock=threading.RLock()
exit_flag=False
thread_lock=threading.Lock()
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_prodcut.start()
thread_consumer.start()
thread_prodcut.join()
thread_consumer.join()
# product(data_queue,exit_flag)