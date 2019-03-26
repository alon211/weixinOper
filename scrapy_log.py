#生成log，定时检查是否由新的Log生成
import os
import datetime
LogList=set()
PATH=r'C:\Users\admin\PycharmProjects\weixinOper\log'
def gernerate_log(save_path,data,file_name):
    '''
    生成Log日志，以文件名+时间保存，以分钟为单位
    :param save_path: log存放路径
    :param data: 写入的数据
    :param file_name: 文件名称
    :return:
    '''
    curtime=datetime.datetime.now().strftime('%Y-%m-%d %H-%M')
    curfile=f'{PATH}\{file_name} {curtime}.txt'
    with open(curfile,'a+') as tmp:
        tmp.write(data+'\n')
def get_newlogset(path,uploadedfiles:set):
    '''
    通过比较已经上传的文件来识别新的文件
    :param path: log存放路径
    :param uploadedfiles: 已经上传的文件名列表
    :return: 未上传的文件名集合
    '''
    # log存放位置所有文件名列表
    files=os.listdir(path)
    files=map(lambda x: os.path.join(path,x),files)
    files=set(files)
    #上传的文件名和存放的文件名列表合集
    allfiles=uploadedfiles|files
    #差集得出没有上传的文件名列表
    unuploadedfiles=allfiles-uploadedfiles
    return unuploadedfiles
def read_uploadedfile(uploadedfile):
    rst=None
    with open(uploadedfile,'r') as f:
        tmp=f.read()
        rst=tmp.split('\n')
        return rst
def save_uploadedfile(uploadedfile,data):
    rst=None
    uploadedfiles=set(read_uploadedfile(uploadedfile))
    uploadedfiles.add(data)
    with open(uploadedfile,'w+') as tmp:
        for data in uploadedfiles:
            tmp.write(data+'\n')
        return True
# save_uploadedfile('uploadedfiles.txt','1.txt')
# save_uploadedfile('uploadedfiles.txt','2.txt')
# print(read_uploadedfile('uploadedfiles.txt'))
gernerate_log(PATH,'123','alarm')
# uploadedfiles={'alarm 2019-03-12 21-42.txt', 'alarm 2019-03-12 20-38-00.txt', 'alarm 2019-03-12 20-59.txt', 'alarm 2019-03-12 20-38-15.txt'}
# print(get_newlogset(PATH,uploadedfiles))