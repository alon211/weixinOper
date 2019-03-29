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
from time import gmtime
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
    # uploadingfiles={}
    # waitinguploadfiles={}
    global waitinguploadfiles
    while not exit_flag :
        logging.info(f'{threading.current_thread().name}:before waitinguploadfiles')
        waitinguploadfiles=waitinguploadfiles|get_newlogset(PATH,uploadedfiles)
        logging.info(f'{threading.current_thread().name}:after waitinguploadfiles')


    # if len(uploadingfiles)!=0:
        #     logging.info(f'{threading.current_thread().name} will get a value from upladedfiles')
        #     value=uploadedfiles.pop()
        #     logging.info(f'{threading.current_thread().name} will put a value')
        #     data.put(value)
        #     logging.info(f'{threading.current_thread().name} have put a value {value}')
        #     logging.info(f'{threading.current_thread().name} : data size  {data.qsize()}')
        # else:
        #     logging.info(f'{threading.current_thread().name} : waiting new file ')
        #     uploadingfiles=get_newlogset(PATH,uploadedfiles)
def manage(*args):
    data,=args
    products=set()
    consumers=set()
    thread_name=threading.current_thread().name
    logging.info(f'{thread_name}: start!')
    global waitinguploadfiles,uploadedfiles,isEmpty
    while True:
        if products == waitinguploadfiles :
            #说明没有新的文件
            logging.info(f'{thread_name}: no new file is producted')
            logging.info(f'{thread_name}: products:{len(products)} waitinguploadfiles:{len(waitinguploadfiles)}')
        else:
            logging.info(f'{thread_name}: we have a new file , update my products')
            products = waitinguploadfiles
            for product in products:
                data.put(product)
                consumers.add(product)
            # isEmpty=False
            # logging.info(f'{thread_name}: isEmpty={isEmpty} 61')
        if data.qsize()==0:
            logging.info(f'{thread_name}: no file is consumer')
            # 并集
            uploadedfiles=uploadedfiles|consumers
            save_uploadedfile('uploadedfiles.txt',uploadedfiles)
        else:
            logging.info(f'{thread_name}: we have  new files want to be  uploaded')
            logging.info(f'{thread_name}: queue size={data.qsize()}')
            # logging.info(f'{thread_name}: isEmpty={isEmpty} 71')

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
            logging.info(f'{threading.current_thread().name}: will get a value')
            value=data.get(timeout=1)
            logging.info(f'{threading.current_thread().name}: will push to git -------------')
            gitcode=git_oper(value)
            logging.info(f'{threading.current_thread().name}: have got a value {value}')
            logging.info(f'{threading.current_thread().name}: gitcode= {gitcode}')
        except Exception as e:
            logging.info(f'Error:{e}')
            # print(status)
            # print(value)
            logging.info(f'the queue is empty,{thread_name}: is waiting a value 92 ')
            # time.sleep(0.1)

            # logging.info(f'{thread_name}: isEmpty={isEmpty} 95')

            # con.notify()
            # con.wait()



PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue(20)
waitinguploadfiles=set()
uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
con=threading.Condition()
isEmpty=True
print(uploadedfiles)
lock1=False
lock2=False
lock=threading.RLock()
exit_flag=False
thread_lock=threading.Lock()
thread_products=[]
thread_consumers=[]
for i in range(5):
    thread_products.append(threading.Thread(target=product,name=f'product{i}',args=(data_queue,exit_flag)))
    thread_consumers.append(threading.Thread(target=consumer,name=f'consumer{i}',args=(data_queue,)))
# thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
# thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_manager=threading.Thread(target=manage,name='manager',args=(data_queue,))
# thread_prodcut.start()
# thread_consumer.start()
for thread_prodcut in thread_products:
    thread_prodcut.start()
    # thread_prodcut.join()
for thread_consumer in thread_consumers:
    thread_consumer.start()
    # thread_consumer.join()

thread_manager.start()
# thread_prodcut.join()
# thread_consumer.join()
# thread_manager.join()
# product(data_queue,exit_flag)