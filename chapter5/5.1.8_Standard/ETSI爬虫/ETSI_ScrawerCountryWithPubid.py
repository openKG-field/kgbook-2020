#
# ETSI_Scrawer_txt_country.py
# @author fan
# @description 
# @created Mon Jun 11 2018 15:04:25 GMT+0800 (中国标准时间)
# @last-modified Tue Jun 19 2018 10:53:44 GMT+0800 (中国标准时间)
#


import requests
import urllib
import time
from bs4 import BeautifulSoup
import re
import requests
import os
import config_set
import json
import time
##由于event_hander相关参数每日保持更新，所以在遇到未知错误时，请首先修改config文件中的时间到2017年任意一天，格式为20170101，目的是更新cfg文件

''''''
def get_event_data(text):
    key=text.get('id')
    value=text.get('value')
    return key,value

def process_event_data(headers):
    url = "https://ipr.etsi.org/SelectPatentLocal.aspx"
    get_event_payload = "txtPublicationNumber=9258835"
    response_event = requests.request("POST", url, data=get_event_payload, headers=headers)
    event_data=BeautifulSoup(response_event.text,'html.parser').find_all('input')
    input_dict={ key:value for key,value in map(get_event_data,event_data)}
    input_dict['DateTime']=time.strftime('%Y,%m,%d',time.localtime(time.time()))
    return input_dict

def get_cookie():
    s = requests.session()
    s.get("https://ipr.etsi.org/SelectPatentLocal.aspx")
    cookie_value = ''
    for x in s.cookies:
        cookie_value += x.name + '=' + x.value + ';'
    cookie_value = cookie_value[:len(cookie_value)-1]
    return cookie_value

def etsi_scrawer(headers,DateTime,etsi_num,__EVENTVALIDATION,__VIEWSTATEGENERATOR,__VIEWSTATE,country):   
    url = "https://ipr.etsi.org/SelectPatentLocal.aspx"
    # payload ="------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ScriptManager1\"\r\n\r\npanelModalPopupPanel|btnSearch\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"FormDecorator1_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"tbPatent_ClientState\"\r\n\r\n{\"selectedIndexes\":[\"0\"],\"logEntries\":[],\"scrollState\":{}}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hfVisibleButton\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hfIDPatent\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hfHandlingControlID\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hfUserID\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hfCreationMode\"\r\n\r\nfalse\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtApplicationNumber\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtApplicationNumber_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"\",\"valueAsString\":\"\",\"lastSetTextBoxValue\":\"\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate$dateInput\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate_dateInput_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"\",\"valueAsString\":\"\",\"minDateStr\":\"1980-01-01-00-00-00\",\"maxDateStr\":\"2099-12-31-00-00-00\",\"lastSetTextBoxValue\":\"\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate_calendar_SD\"\r\n\r\n[]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate_calendar_AD\"\r\n\r\n[[1980,1,1],[2099,12,30],[%s]]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtPublicationNumber\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtPublicationNumber_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"%s\",\"valueAsString\":\"%s\",\"lastSetTextBoxValue\":\"%s\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate$dateInput\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate_dateInput_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"\",\"valueAsString\":\"\",\"minDateStr\":\"1980-01-01-00-00-00\",\"maxDateStr\":\"2099-12-31-00-00-00\",\"lastSetTextBoxValue\":\"\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate_calendar_SD\"\r\n\r\n[]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate_calendar_AD\"\r\n\r\n[[1980,1,1],[2099,12,30],[%s]]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtTitle\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtTitle_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"\",\"valueAsString\":\"\",\"lastSetTextBoxValue\":\"\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hdnCompId\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"grpSearch\"\r\n\r\nrbCountry\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ddlCountry\"\r\n\r\n---Select country---\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ddlCountry_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ddlOrganisation\"\r\n\r\n---Select organization---\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ddlOrganisation_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ResultRadGrid_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"pgvwPatent_ClientState\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTTARGET\"\r\n\r\nbtnSearch\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTARGUMENT\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATEGENERATOR\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTVALIDATION\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__ASYNCPOST\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"RadAJAXControlID\"\r\n\r\nRadAjaxManagerProxy1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"%(DateTime,etsi_num,etsi_num,etsi_num,etsi_num,DateTime,__VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION)
    payload="------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ScriptManager1\"\r\n\r\npanelModalPopupPanel|btnSearch\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtAppDate_calendar_AD\"\r\n\r\n[[1980,1,1],[2099,12,30],[%s]]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtPublicationNumber\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtPublicationNumber_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"%s\",\"valueAsString\":\"%s\",\"lastSetTextBoxValue\":\"%s\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"dtPubDate_calendar_AD\"\r\n\r\n[[1980,1,1],[2099,12,30],[%s]]\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"txtTitle_ClientState\"\r\n\r\n{\"enabled\":true,\"emptyMessage\":\"\",\"validationText\":\"\",\"valueAsString\":\"\",\"lastSetTextBoxValue\":\"\"}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"grpSearch\"\r\n\r\nrbCountry\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ddlCountry\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTTARGET\"\r\n\r\nbtnSearch\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATEGENERATOR\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTVALIDATION\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__ASYNCPOST\"\r\n\r\ntrue\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"RadAJAXControlID\"\r\n\r\nRadAjaxManagerProxy1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"%(DateTime,etsi_num,etsi_num,etsi_num,etsi_num,DateTime,country,__VIEWSTATE,__VIEWSTATEGENERATOR,__EVENTVALIDATION)
    response = requests.request("POST", url, data=payload, headers=headers)
    return response

def process_response(req):
    soup=BeautifulSoup(req,'html.parser')
    res=soup.find(name='div',id='ResultRadGrid')
    head=res.find('tr').find_all('th')
    body=res.find('tr',attrs='Table_Body').find_all('td')
    dict={}
    for index,head in enumerate(head):
        dict[head.text]=body[index-1].text
    return dict

def process_response_excel(req):
    soup=BeautifulSoup(req,'html.parser')
    try:
        res=soup.find(name='div',id='ResultRadGrid')
        no=res.find('tr',attrs='rgNoRecords')
        head=list([i.text for i in res.find('tr').find_all('th')]) 
        body=list([no.text]) 
        return 0,tuple([head,body])
    except:
        # res=soup.find(name='div',id='ResultRadGrid')
        head=list([i.text for i in res.find('tr').find_all('th')]) 
        body=list([i.text for i in res.find('tr',attrs='Table_Body').find_all('td')])   
        return 1,tuple([head,body])

import xlwt

def fuction_with_excel(data,publicNum):
    workbook=xlwt.Workbook(encoding='utf-8')  
    booksheet=workbook.add_sheet('default', cell_overwrite_ok=True)   
    for i,row in enumerate(data):  
        for j,col in enumerate(row):  
            booksheet.write(i,j,col)
    workbook.save('%s.xls'%publicNum)  

def fuction_with_excel_no_res(data,publicNum):
    workbook=xlwt.Workbook(encoding='utf-8')  
    booksheet=workbook.add_sheet('default', cell_overwrite_ok=True)   
    for i,row in enumerate(data):  
        for j,col in enumerate(row):  
            booksheet.write(i,j,col)
    booksheet.merge(1,1,0,len(data[0])-1)
    workbook.save('%s.xls'%publicNum) 

def struct_header():
    cookie_value=get_cookie()
    headers={
        'accept': "*/*",
        'accept-language': "zh-CN,zh;q=0.9",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cookie': cookie_value,
        'host': "ipr.etsi.org",
        'origin': "https://ipr.etsi.org",
        'referer': "https://ipr.etsi.org/SelectPatentLocal.aspx?uniqueId=ucPatent",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        'x-microsoftajax': "Delta=true",
        }
    return headers

def main():
    config_path='./data.cfg'
    headers=struct_header()
    DateTime=time.strftime('%Y,%m,%d',time.localtime(time.time()))
    config_setter=config_set.my_cfg_setter(config_path)
    section='ETSI_EVENT_DATA'
    if(config_setter.get_value(section,'DateTime')!=DateTime):
        try:
            event_data=process_event_data(headers)
            config_setter.put_item_batch(section,event_data)
        except:
            print('insert data into config failed')
    __EVENTVALIDATION=config_setter.get_value(section,'__EVENTVALIDATION')
    __VIEWSTATE=config_setter.get_value(section,'__VIEWSTATE')
    __VIEWSTATEGENERATOR=config_setter.get_value(section,'__VIEWSTATEGENERATOR')
    with open('t.txt','r') as f_r:
        li=f_r.readlines()
        etsi_num_list=[i.strip() for i in li]
    cont=0
    with open('country.json','r') as f_r:
        country_dict=json.load(f_r)
    for etsi_num in etsi_num_list:
        # if cont%3==0:headers=struct_header()
        flag=True;itero=0
        if len(etsi_num)==0:continue
        country=country_dict[etsi_num[:2]]
        c0=etsi_num[:2]
        etsi_num=re.sub('\D','',etsi_num)     
        print(etsi_num)
        while flag:
            cont+=1
            try:
                response=etsi_scrawer(headers,DateTime,etsi_num,__EVENTVALIDATION,__VIEWSTATEGENERATOR,__VIEWSTATE,country)
                re_flag,etsi_out=process_response_excel(response.text)
                if etsi_out[1][0][:2]!=c0:
                    # fuction_with_excel_no_res(etsi_out,etsi_num)
                    print('no-result')
                elif re_flag:
                    fuction_with_excel(etsi_out,etsi_num)
                else:print('no-result')
                    # fuction_with_excel_no_res(etsi_out,etsi_num)
                flag=False
            except Exception as e :
                print(e)
                headers=struct_header()
                if itero<3:
                    itero+=1
                    print('将进行第%d轮重试'%(itero))
                else:flag=False
    return 

if __name__ == '__main__':
    main()
