import threading
from scrapy_log import *

def p(*args):
    num,=args
    for i in range(num):
        # with open('failuploadedfiles.txt','a+') as f:
        #     f.write(f'product{i}'+'\n')
        save_uploadedfile('failuploadedfiles.txt',{f'product{i}'})
def c(*args):
    num,=args
    for i in range(num):
        # with open('failuploadedfiles.txt','a+') as f:
        #     f.write(f'consumer{i}'+'\n')
        save_uploadedfile('failuploadedfiles.txt',{f'consumer{i}'})

thread_prodcut=threading.Thread(target=p,name='product',args=(5,))
thread_consumer=threading.Thread(target=c,name='product',args=(5,))

thread_prodcut.start()
thread_consumer.start()