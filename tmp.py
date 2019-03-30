import threading
from scrapy_log import *
import time
import atexit
import signal
import sys
import traceback
def term_sig_handler(signum, frame):
    print( 'catched singal: %d' % signum)
    sys.exit()

@atexit.register
def atexit_fun():
    print (f'i am exit, stack track:{n}')

    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)

def p(*args):
    num,=args
    global n
    while True:
        n=n+2
        # with open('failuploadedfiles.txt','a+') as f:
        #     f.write(f'product{i}'+'\n')
        save_uploadedfile('failuploadedfiles.txt',{f'product{n}'})
        time.sleep(0.1)
def c(*args):
    num,=args
    global n
    while True:

        n=n+1
        # with open('failuploadedfiles.txt','a+') as f:
        #     f.write(f'consumer{i}'+'\n')
        save_uploadedfile('failuploadedfiles.txt',{f'consumer{n}'})
        time.sleep(0.1)
if __name__=='__main__':
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    n=0
    thread_prodcut=threading.Thread(target=p,name='product',args=(5,))
    thread_consumer=threading.Thread(target=c,name='product',args=(5,))

    thread_prodcut.start()
    thread_consumer.start()