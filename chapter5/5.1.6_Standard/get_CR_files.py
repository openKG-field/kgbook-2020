#-*- encoding:'utf-8' -*-

import urllib.parse
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import requests
import os
import mutidownload

# params  CategoryId=808 CategoryType=SiteHome ItemListActionName=PostList PageIndex=3 ParentCategoryId=0 TotalPostCount=4000
def getHtml(url,values):
    user_agent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    headers = {'User-Agent':user_agent}
#     data = urllib.parse.urlencode(values)
#     response_result = urllib.request.urlopen(url+'?'+data).read()
    try:
        response_result = urllib.request.urlopen(url,timeout=100).read()
        html = response_result.decode('utf-8')
        return html
    except:
        return None

#获取数据
def requestUrl(url,index=1):
 #   print('请求数据')
#    url = 'http://www.3gpp.org/ftp/Specs/archive/00_series/'
    value= {
         'CategoryId':808,
         'CategoryType' : 'SiteHome',
         'ItemListActionName' :'PostList',
         'PageIndex' : index,
         'ParentCategoryId' : 0,
        'TotalPostCount' : 4000
    }
    result = getHtml(url,value)
    return result

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

def process_archive(req,header='http://www.3gpp.org'):    
    soup=BeautifulSoup(req,'html.parser')
    find=soup.find_all(name='a')
    href=[i.get('href') for i in find]      #header='http://www.3gpp.org'
    href_has_child=[];href_to_save=[]
    for item in href:
        if item.endswith('/'):
            href_has_child.append(header+item)
        else:
            href_to_save.append(header+item)
    return href_has_child[1:],href_to_save

def save_series_files(parent_url):
    parent_page=requestUrl(parent_url)
    if parent_page==None:
        return
    local_path='D:/Document/WorkSpace/专利与标准/爬虫'
    log_path='D:/Document/WorkSpace/专利与标准/爬虫/Script/TSG_log_file.txt'
    header='http://www.3gpp.org';ftp_body='/ftp/tsg_cn';series_url_parent='/TSG_CN'
    page_has_child,files_to_save=process_archive(parent_page)
    slice_dist=len(header+ftp_body)
    local_dir_parent=local_path+parent_url[slice_dist:]
    if not os.path.exists(local_dir_parent):
        os.makedirs(local_dir_parent)
    for item in files_to_save:
        save_file_path=local_path+item[slice_dist:]
        if os.path.exists(save_file_path) and os.path.getsize(save_file_path):
            pass
        else:
            r=requests.head(item)
            if int(r.headers['content-length'])>200000:
                mutidownload.download_file(item,save_file_path,log_path,num_thread=10)
            else:
                save_net_files(item,save_file_path,log_path)
    if not len(page_has_child):
        return
    for item in page_has_child:
        save_series_files(item)
    
def main():
    req=requestUrl("http://www.3gpp.org/ftp/tsg_cn/TSG_CN/")
    parent_to_find,parent_has_child=process_archive(req)
    for i in parent_to_find[10:15]:
        save_series_files(i)

if __name__ == '__main__':
    main()
