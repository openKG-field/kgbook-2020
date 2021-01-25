
# coding: utf-8

# In[1]:


# coding: utf-8
# In[14]:
import requests
import codecs
import random
import time
import json
import urllib.request
import re
import pytesseract
import lxml
import sys
from selenium import webdriver
#from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from http import cookiejar
from urllib import request
from urllib import parse
from urllib import error
from PIL import Image

def get_login(text):
    bs = BeautifulSoup(text, "html.parser")
    div = bs.find("div", class_="wrap-left")
    a = div.find("a", class_="login-btn")
    href = a.get("href")
    href = 'http://www.pss-system.gov.cn' + href
    return href

def login(href_log):
    browser.get(href_log)
    browser.save_screenshot(r'fcode.png')
    elem_code = browser.find_element_by_id("codePic")
    left = elem_code.location['x']
    top = elem_code.location['y']
    elementWidth = elem_code.location['x'] + elem_code.size['width']
    elementHeight = elem_code.location['y'] + elem_code.size['height']
    picture = Image.open(r'fcode.png')
    picture = picture.crop((left, top, elementWidth, elementHeight))
    picture.save(r'code.png')
    
    #验证码识别
def code(name):
    threshold = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 78, 80, 85, 90, 95, 100, 105, 110, 115, 120]
    tableList = []
    for j in threshold:
        table = []    
        for i in range(256):    
            if i < j:    
                table.append(0)    
            else:    
                table.append(1) 
        tableList.append(table)   
    rep = {
        'O':'0',
        'M':'9',
        'L':'1',
        'Z':'2',
        'S':'8',
        '§':'5',
        '.':'0',
        '\n':'0',
        '=':'0',
        ' ':''
    }
    #name = 'code.png'
    im = Image.open(name)    
    imgry = im.convert('L')
    text = pytesseract.image_to_string(imgry)
    imgry.save('g'+name)
    for i in tableList:
        out = imgry.point(i,'1')  
        out.save('b'+name)    
        text = pytesseract.image_to_string(out)    
        text = text.strip()
        for r in rep:
            text = text.replace(r, rep[r])
    return text

#识别出的字符处理
def code_handle(text):
    num_1 = int(text[0] + text[1])
    num_2 = int(text[3])
    if text[2] == "+":
        final = num_1 + num_2
    else:
        final = num_1 - num_2
    return final

def login_act(browser, final):
    elem_user = browser.find_element_by_name("j_username")
    elem_user.send_keys("moqiu_test1")
    elem_pass = browser.find_element_by_id("j_password_show")
    elem_pass.send_keys("abc123456")
    elem_valid = browser.find_element_by_id("j_validation_code")
    elem_valid.send_keys(final)
    elem_btn = browser.find_element_by_class_name("btn")
    elem_btn.click()
    time.sleep(5)
    
    elem_gen_head = browser.find_element_by_id("gen_head")
    elem_gen_head.click()
    time.sleep(5)
    browser.switch_to_window(browser.window_handles[1])
    elem_tableSearch = browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/ul/li[3]/a")
    elem_tableSearch.click()
    time.sleep(5)
    browser.execute_script("window.scrollBy(0, 400)")
    elem_select_btn = browser.find_element_by_xpath("//*[@id='IVDB007select']")
    elem_select_btn.click()
    time.sleep(1)
    elem_select_time = browser.find_element_by_xpath("//*[@id='IVDB007select']/a/ul/li[6]")
    elem_select_time.click()
    elem_input = browser.find_element_by_id("tableSearchItemIdIVDB007")
    elem_input.send_keys("20170101 20170201")
    elem_ipc = browser.find_element_by_id("tableSearchItemIdIVDB045")
    elem_search = browser.find_element_by_xpath("/html/body/div[3]/div[3]/div/div[2]/div[3]/a[3]")
    elem_search.click()
    time.sleep(10)
    browser.execute_script("window.scrollBy(0, 200)")
    elem_to_list = browser.find_element_by_xpath("//*[@id='result_view_mode']/a[2]")
    elem_to_list.click()
    time.sleep(5)
    browser.execute_script("window.scrollBy(0, 200)")
    return browser

    
def find_patent(browser):
    #topic_name; info_box; abstract; content;
    time.sleep(5)
    elem_btn_details = browser.find_elements_by_class_name("full-text_sm")
    i = 0
    for elem_btn_detail in elem_btn_details:
        redict = {'topic_name':"",'info_box':{},'abstract':"",'content':"",'attribute':{}}
        elem_btn_tmps = browser.find_elements_by_class_name("full-text_sm")
        elem_btn_tmp = elem_btn_tmps[i]
        elem_btn_tmp.click()
        time.sleep(0.5)
        browser.switch_to_window(browser.window_handles[2])
        time.sleep(8)
        while True:
            try:
                html_text = browser.page_source#第一个界面
                bs = BeautifulSoup(html_text, "html.parser")
                try:
                    topic_name = bs.find("div", class_="table-container-title").text
                except AttributeError:
                    topic_name = "无标题"
                try:
                    div = bs.find("div", class_="table-container")
                    table = div.find("table")
                    tr_list = table.find_all("tr")
                except AttributeError:
                    div_list = bs.find_all("div", class_="table-container")
                    table = div_list[1].find("table")
                    tr_list = table.find_all("tr")
                break
            except IndexError:
                browser.refresh()
                time.sleep(10)
        tr = tr_list[0]
        td_list = tr.find_all("td")
        td = td_list[1].text
        info_box = {}
        attribute = {'law_condition':[],'yinzheng':[],'tongzu':''}
        for tr in tr_list:
            key = tr.find("td", class_="first-td").text
            value = tr.find("td", class_="second-td").text
            info_box[key] = value
        abstract = bs.find("div", class_="abstract-content").text
        redict['abstract'] = abstract
        redict['topic_name'] = topic_name
        redict['info_box'] = info_box
        time.sleep(5)
        elem_btn_all = browser.find_element_by_xpath("//li[@id='fullTextTitleId']/a")
        elem_btn_all.click()
        time.sleep(10)
        html_text = browser.page_source#全文
        bs = BeautifulSoup(html_text,"html.parser")
        div = bs.find("div", id="lawStateContainerId")
            
        law_condition = []
        yinzheng = []
        tongzu = []
        try:
            ul = div.find("ul")
            li_list = ul.find_all("li")
            for li in li_list:
                span_list = li.find_all("span")
                for span in span_list:
                    law_condition.append(span.text)
            attribute['law_condition'] = law_condition
        except AttributeError:
            law_condition.append("无法律状态数据")
            attribute['law_condition'] = law_condition
        div = bs.find("div", id="patcitContainerId")
        try:
            ul = div.find("ul")
            li_list = ul.find_all("li")
            for li in li_list:
                span_list = li.find_all("span")
                for span in span_list:
                    yinzheng.append(span.text)
            attribute['yinzheng'] = yinzheng
        except AttributeError:
            yinzheng.append("无引证文献数据")
            attribute['yinzheng'] = yinzheng
        div = bs.find("div", id="cognationContainerId")
        try:
            ul = div.find("ul")
            li_list = ul.find_all("li")
            for li in li_list:
                span_list = li.find_all("span")
                for span in span_list:
                    tongzu.append(span.text)
            attribute['tongzu'] = tongzu
        except AttributeError:
            tongzu.append("无同族文献数据")
            attribute['tongzu'] = tongzu
        redict['attribute'] = attribute
        
        text = []
        try:
            div_list = bs.find_all("div", class_="fullText")
            for div in div_list:
                table = div.find("table")
                tr_list = table.find_all("tr")
                for tr in tr_list:
                    td_text = tr.find("td").text
                    text.append(td_text)
        except AttributeError:
            text.append("None")
            div = bs.find("div", class_="fulltext-tab-content").text
            text.append(div)
        redict['content'] = text
        if len(text) < 10:
            print("ok")
            print(td)
            f.write(td + "\r\n")
        write_file(redict, topic_name)
        browser.close()
        time.sleep(0.5)
        while True:
            try:
                browser.switch_to_window(browser.window_handles[1])
                break
            except IndexError:
                browser.refresh()
                time.sleep(5)
        browser.execute_script("window.scrollBy(0, 80)")
        i += 1
    browser.execute_script("window.scrollBy(0, -700)")
    next_page(browser)
    find_patent(browser)
    
def next_page(browser):
    time.sleep(10)
    while True:
        try:
            elem_control_page = browser.find_elements_by_xpath("//div[@class='page_top']/a")
            break
        except NoSuchElementException:
            browser.refresh()
            time.sleep(8)
    elem_next_page = elem_control_page[2]
    elem_next_page.click()


def write_file(redict ,topic_name):
    topic_name = topic_name.replace("/","")
    topic_name = topic_name.replace(" ",",")
    with open("D://Wiki_analysis//国知局//"+topic_name+".json","w+",encoding="utf-8") as f:
            json.dump(redict,f,ensure_ascii=False)
    
if __name__ == '__main__':
    url = 'http://www.pss-system.gov.cn/sipopublicsearch/portal/uiIndex.shtml'
#    option = webdriver.ChromeOptions()
#    option.add_argument('headless')
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    content = browser.page_source
    href_log = get_login(content)
    login(href_log)
    text = code('code.png')
    final = code_handle(text)
    browser = login_act(browser, final)

    f = codecs.open("D://Wiki_analysis//国知局//notext.txt","a",encoding="utf-8")
    page = 1
    while page < 1:
        next_page(browser)
        page += 1
    find_patent(browser)
    f.close()
    browser.quit()

