import sys
import requests
import threading
import datetime
import time
import os
import urllib
import urllib.request 
 
# 传入的命令行参数，要下载文件的url
# url = sys.argv[1]

def Handler(start, end, url, file_path,log_path):
    try:    
        headers = {'Range': 'bytes=%d-%d' % (start, end)}
        r = requests.get(url, headers=headers, stream=True,timeout=30)
        
        # 写入文件对应位置
        with open(file_path, "r+b") as fp:
            fp.seek(start)
            var = fp.tell()
            fp.write(r.content)
    except:
        with open(log_path,'a') as log_f:
            log_f.writelines(file_path+' save failed\n')
            print(file_path+' save failed\n')
            os.remove(file_path)
            return 
    return 
        
def download_file_Threading(url,file_path,log_path,num_thread = 5):    
    r = requests.head(url)
    try:
        #file_name = url.split('/')[-1]
        file_size = int(r.headers['content-length'])   # Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
    except:
        print("检查URL，或不支持对线程下载")
        return
 
    #  创建一个和要下载文件一样大小的文件
    fp = open(file_path, "wb")
    fp.truncate(file_size)
    fp.close() 
    # 启动多线程写文件
    part = file_size // num_thread  # 如果不能整除，最后一块应该多几个字节
    for i in range(num_thread):
        start = part * i
        if i == (num_thread - 1):   # 最后一块
            end = file_size
        else:
            end = start + part 
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'file_path': file_path,'log_path':log_path})
        
        t.setDaemon(True)
        t.start()
    # 等待所有线程下载完成
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % (file_path))
    return

def save_net_files(file_url,save_path,log_path):
    try:
        with urllib.request.urlopen(file_url,timeout=30) as request_file:
            with open(save_path,'wb') as f_save:
                f_save.write(request_file.read())
                f_save.flush()
                f_save.close()
                print(file_url+' download sucess.')
    except:
        with open(log_path,'a') as log_file:
            log_file.writelines(file_url+'\n')
            log_file.flush()
            log_file.close()
            print(file_url+' save failed.')
    return

def download_web_file(local_file_path,net_file_path,log_path):
    '''local_file_path,net_file_path,log_path,the program contains a check of the exists of the download file'''
    if os.path.exists(local_file_path) and os.path.getsize(local_file_path):
        pass
    else:
        try:
            r=requests.head(net_file_path)
        except:
            print('get informathin of %s failed.'%net_file_path)
        try:
            if int(r.headers['content-length'])>200000:
                download_file_Threading(net_file_path,local_file_path,log_path,num_thread=10)
            else:
                save_net_files(net_file_path,local_file_path,log_path)
        except:
            pass