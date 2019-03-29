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
    global waitinguploadfiles,uploadedfiles,isEmpty,notify_p_to_m,notify_m_to_c,failuploaded_queue,notify_c_to_m
    while True:


        # logging.info(f'{threading.current_thread().name}: 54 notify_p_to_m={notify_p_to_m}')
        if notify_p_to_m:
            products=waitinguploadfiles
            notify_p_to_m=False
        tmp_failupload_files=set(read_uploadedfile('failuploadedfiles.txt'))
        if tmp_failupload_files!=set():
            logging.info(f'{threading.current_thread().name}: 58 tmp_failupload_files={len(tmp_failupload_files)}')
            for file in tmp_failupload_files:
                products.add(file)
            clear_file('failuploadedfiles.txt')

            # logging.info(f'{threading.current_thread().name}: 58 notify_p_to_m={notify_p_to_m}')
        # logging.info(f'{threading.current_thread().name}:products={len(products)},waitinguploadfiles={len(waitinguploadfiles)}')

    # 将products传入consumer
        logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
        if not notify_m_to_c and len(products)>0:#需要consumer确认收到数据后再解锁
            logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
            value=products.pop()
            data.put(value)
            notify_m_to_c = True
            logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
        # 防止多个consumer同时在对failuploadedfiles操作，所有manage操作时锁住所有consumer
        try:
            value=failuploaded_queue.get(timeout=0.1)
            save_uploadedfile('failuploadedfiles.txt',{value})
        except:
            pass
        if notify_c_to_m:

           notify_c_to_m=False

# 模拟上传文件
def consumer(*args):
    data,=args
    thread_name=threading.current_thread().name
    logging.info(f'{thread_name}: start!')
    isuploaded=True
    status=None
    global notify_m_to_c,notify_c_to_m,failuploaded_queue
    while True:
        if notify_m_to_c and not notify_c_to_m:

            logging.info(f'{threading.current_thread().name}:notify_m_to_c={notify_m_to_c}')
            try:
                logging.info(f'{threading.current_thread().name}: will get a value')
                value=data.get(timeout=1)
                logging.info(f'{threading.current_thread().name}: will push to git -------------')
                gitcode=git_oper(value)
                logging.info(f'{threading.current_thread().name}: gitcode= {gitcode}')
                status=gitcode[0]
                # 上传失败的status为False，将失败的存入failuploadedfiles.txt
                if not status :
                    # save_uploadedfile('failuploadedfiles.txt', {value})
                    failuploaded_queue.add(value)
                    notify_c_to_m=True
                notify_m_to_c=False
            except Exception as e:
                # logging.info(f'Error:{e}')
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

notify_p_to_m=False
notify_m_to_c=False
notify_c_to_m=False
failuploaded_queue=queue.Queue()
print(uploadedfiles)
lock1=False
lock2=False
lock=threading.RLock()
exit_flag=False
thread_lock=threading.Lock()
thread_products=[]
thread_consumers=[]
# for i in range(5):
#     thread_products.append(threading.Thread(target=product,name=f'product{i}',args=(data_queue,exit_flag)))
#     thread_consumers.append(threading.Thread(target=consumer,name=f'consumer{i}',args=(data_queue,)))
thread_prodcut=threading.Thread(target=product,name='product',args=(data_queue,exit_flag))
thread_consumer=threading.Thread(target=consumer,name='consumer',args=(data_queue,))
thread_manager=threading.Thread(target=manage,name='manager',args=(data_queue,))
thread_prodcut.start()
thread_consumer.start()
# for thread_prodcut in thread_products:
#     thread_prodcut.start()

# for thread_consumer in thread_consumers:
#     thread_consumer.start()


thread_manager.start()
# thread_prodcut.join()
# thread_consumer.join()
# thread_manager.join()
# product(data_queue,exit_flag)