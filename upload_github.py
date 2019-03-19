# import requests
# import base64
# headers={'Authorization':'token 379b34b38284037947b6c30254f28f3addcb611d'}
# # response=requests.get('https://api.github.com/user',headers=headers)
# payload={'message':'my new file contents',
#          'content':base64.b64encode('erro log'.encode('utf-8')).decode()
#          }
# url='https://api.github.com/repos/alon211/weixinOper/contents/log/2.txt'
# response=requests.put(url,headers=headers,json=payload)
# print(response.url)
# # 创建文件成功，返回201
# print (response.status_code)
# # print(response.json())
import datetime
import subprocess
def git_oper(file):
    status=subprocess.run(['git','add',file])
    if status.returncode!=0:
        return False,status.returncode
    status=subprocess.run(['git','commit','-m',datetime.datetime.now().strftime('%Y-%m-%d %H-%M')])
    if status.returncode!=0:
        return False,status.returncode
    status=subprocess.run(['git','push','--set-upstream','origin','master'])
    if status.returncode!=0:
        return False,status.returncode
    return True,status.returncode
# status=git_oper('1.txt')
# status=subprocess.run(['git','add','log/alarm 2019-03-12 20-38-00.txt'])
# print(status)
# status=subprocess.run(['git','commit','-m',datetime.datetime.now().strftime('%Y-%m-%d %H-%M')])
# print(status)
# status=subprocess.run(['git','push','--set-upstream','origin','master'])
# print(status)