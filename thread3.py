#扫描log文件夹内是否有新文件有的话，上传至github

# 创建thread3的异步程序:
# 1.product读取更新文件在同个线程内，只要读到有更新，就把新的路径添加到文件里去，不管最后是否上传成功
# 2.增加manager函数进行中转调度处理
# 3.consumer只进行队列的操作，保证异步时数据的同步性。如果上传失败立马再次放入队列中
# 4.未完善的是退出后如何将队列中未上传的变量保存到上传失败文件中

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
    global waitinguploadfiles,notify_p_to_m,uploadedfiles
    while not exit_flag :
        logging.info(f'{threading.current_thread().name}:before waitinguploadfiles')
        uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
        waitinguploadfiles=get_newlogset(PATH,uploadedfiles)
        if waitinguploadfiles!=set():
            #重新更新保存文件，说明product流程已经拿出来，不需要再次拿了，如果后面上传失败是返工步骤，另外找方法对应
            save_uploadedfile('uploadedfiles.txt',waitinguploadfiles)
            notify_p_to_m=True
            logging.info(f'{threading.current_thread().name}:notify_p_to_m={notify_p_to_m}')


def manage(*args):
    # 写入和读取文件这种操作必须放在唯一的一个线程内。

    data,=args
    products=set()
    consumers=set()
    thread_name=threading.current_thread().name
    logging.info(f'{thread_name}: start!')
    global waitinguploadfiles,uploadedfiles,isEmpty,notify_p_to_m,notify_m_to_c,notify_c_to_m
    while True:
        if notify_p_to_m:
            products=waitinguploadfiles
            notify_p_to_m=False

        logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
        # if not notify_m_to_c and len(products)>0:#需要consumer确认收到数据后再解锁
        if len(products)>0:
            logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
            value=products.pop()
            data.put(value)
            logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')



# 模拟上传文件
def consumer(*args):
    data,=args
    thread_name=threading.current_thread().name
    logging.info(f'{thread_name}: start!')
    isuploaded=True
    status=None
    global notify_m_to_c,notify_c_to_m,failuploaded_queue
    while True:
        if True:

            logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
            try:
                logging.info(f'{threading.current_thread().name}: will get a value')
                value=data.get(timeout=1)
                logging.info(f'{threading.current_thread().name}: will push to git -------------{value}')
                gitcode=git_oper(value)
                logging.info(f'{threading.current_thread().name}: gitcode= {gitcode}')
                status=gitcode[0]
                print(status)
                # 上传失败的status为False，将失败的再次放入队列中
                if not status :
                    data.put(value)

            except Exception as e:
                logging.info(f'the queue is empty,{thread_name}: is waiting a value 92 ')

PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
data_queue=queue.Queue()
waitinguploadfiles=set()
uploadedfiles=set(read_uploadedfile('uploadedfiles.txt'))
con=threading.Condition()
isEmpty=True

notify_p_to_m=False
notify_m_to_c=False
notify_c_to_m=False
failuploaded_queue=queue.Queue()
# print(uploadedfiles)
lock1=False
lock2=False
lock=threading.RLock()
exit_flag=False
thread_lock=threading.Lock()
thread_products=[]
thread_consumers=[]
for i in range(5):
    # thread_products.append(threading.Thread(target=product,name=f'product{i}',args=(data_queue,exit_flag)))
    thread_consumers.append(threading.Thread(target=consumer,name=f'consumer{i}',args=(data_queue,)))
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
# thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_manager=threading.Thread(target=manage,name='manager',args=(data_queue,))

# thread_consumer.start()
# for thread_prodcut in thread_products:
#     thread_prodcut.start()

for thread_consumer in thread_consumers:
    thread_consumer.start()

thread_prodcut.start()
thread_manager.start()
# thread_prodcut.join()
# thread_manager.join()
# product(data_queue,exit_flag)