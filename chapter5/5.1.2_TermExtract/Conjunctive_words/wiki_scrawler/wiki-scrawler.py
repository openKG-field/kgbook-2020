from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
from urllib.request import Request
import re
import logging_module
import json
import time

class MyRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, hdrs):
        return fp

def getStatusCode(url,data_in):
    myHandler = MyRedirectHandler()
    opener = urllib.request.build_opener(myHandler)
    header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    req = Request(url,headers=header,data=data_in)
    # req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0')
    res = opener.open(req,timeout=70)
    return res

# def getStatusCode(url):
#     myHandler = MyRedirectHandler()
#     opener = urllib.request.build_opener(myHandler)
#     req = Request(url)
#     req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')
#     res = opener.open(req)
#     return res

def get_wiki_page(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    req = Request(url, headers=header)
    page=urlopen(req,timeout=70).read().decode('utf-8')
    soup=BeautifulSoup(page,'html.parser')
    return soup

def resOrDisambi(soup):
    return len(soup.find_all(name='table',id='disambigbox'))

def process_nonRes_words(soup):
    extends={}
    for item in soup.find('ul',attrs='mw-search-results').find_all('li'):
        key_ex=item.find('div',attrs='mw-search-result-heading').text
        value_ex=item.find('div',attrs='searchresult').text
        extends[key_ex]=value_ex
    return extends

def process_ambig_words(soup):
    head='https://zh.wikipedia.org'
    href=[]
    ambig_nun=[]
    # itero=0
    for item in soup.find('div',id='mw-content-text').find_all('li'):
        try:
            # print(itero,'.',item.find('a').text)
            ambig_nun.append(item.find('a').text)
            # itero+=1
            href.append(head+item.find('a').get('href'))
        except:
            pass
    return ambig_nun,href

# def process_ambig_eords_no_to_log(soup):
#     head='https://zh.wikipedia.org'
#     href=[]
#     itero=0
#     for item in soup.find('div',id='mw-content-text').find_all('li'):
#         try:
#             # print(itero,'.',item.find('a').text)
#             itero+=1
#             href.append(head+item.find('a').get('href'))
#         except:
#             pass
#     return href

class WikiNormal(object):
    def __init__(self,soup):
        self.soup=soup.find('div',attrs='mw-body-content',id='bodyContent')
        self.cols=[]
        self.head=self.parse_head(soup)
        self.abstract=[]
        self.parse_cols()
        self.block=dict({key:list([]) for key in self.cols})
        self.foot_table=self.parse_foot_table()
        self.table=self.parse_table()
        self.cat=self.parse_catlinks()
        self.parse_content()
        self.all_content={}
        for item in soup.find_all('ul'):
            self.update_ul(item)
        for item in soup.find_all('ol'):
            self.update_ul(item)
        self.set_all_content()
    def parse_head(self,soup):
        title=soup.find_all(name='h1',attrs='firstHeading')
        if len(title)==1:
            return title[0].text
        else:
            return "这是个神奇的网页，有多个主题词"
    def parse_head2(self,soup_loc):
        try:
            head2=soup_loc.find(name='span',attrs='mw-headline')
            return head2.text
        except:
            return None
    def parse_cols(self):
        for item in self.soup.find_all('h2'):
            if item.find(name='span',attrs='mw-headline'):
                self.cols.append(item.find(name='span',attrs='mw-headline').text)
    def parse_ul(self,soup_loc):
        return soup_loc.text
    def parse_table(self):
        tables={}
        itero=0
        for item in self.soup.find_all('table'):
            if not item:
                continue
            if not  item.get('class'):
                continue
            if ('navbox' in item.get('class')) or ('navbox-inner' in item.get('class')) :
                continue
            else:
                title=item.get('class')[0]
                if tables.get(title):
                    title=title+'%s'%itero
                    itero+=1
                tables[title]={}
                for var in item.find_all('th'):
                    value=var.find_next('td').text
                    tables[title][var.text]=value   
        return tables
    def update_ul(self,soup_loc):
        text=self.parse_ul(soup_loc)
        bro_para=soup_loc.find_previous('p')
        bro_head2=soup_loc.find_previous('h2')
        head2=self.parse_head2(bro_head2)
        parent=soup_loc.parent.get('id')
        if (not head2) or (parent in ['mw-hidden-catlinks','mw-normal-catlinks','footer']) :
            return
        if bro_para.find_previous('h2') and (bro_para.find_previous('h2')==bro_head2):
            temp=self.block[head2]
            temp.insert(temp.index(bro_para.text)+1,text)
            self.block[head2]=temp
        else:
            self.block[head2].append(text)
    def parse_content(self):
        for item in self.soup.find_all('p'):
            if item.find_previous(name='h2'):
                col,para=self.parse_colsAndPara(item)
                if col:
                    self.block[col].append(para)
            elif item.find_previous(name='h1'):
                self.abstract.append(item.text)
    def parse_colsAndPara(self,soup_loc):
        return self.parse_head2(soup_loc.find_previous('h2')),soup_loc.text
    def parse_foot_table(self):
        tbody={}
        for item in self.soup.find_all('table',attrs='navbox-inner'):
            itero=1
            title=item.find('th',attrs='navbox-title')
            try:
                title=title.find_all('div')[1].text
            except:
                title=itero
                itero+=1
            tbody[title]={}
            for var in item.find_all('th',scope='row',attrs='navbox-group'):
                value=var.find_next('td').text
                tbody[title][var.text]=value
        return tbody
    def parse_normal_table(self,soup_loc):
        return
    def parse_catlinks(self):
        soup_loc=self.soup.find('div',attrs='mw-normal-catlinks')
        return [i.text for i in soup_loc.find_all('a')]
    def set_all_content(self):
        self.all_content['topic_word']=self.head
        self.all_content['abstract']=""
        for para in self.abstract:
            self.all_content['abstract']+=para
        self.all_content['cols']=self.cols
        self.all_content['body']=[]
        for col in self.cols:
            paras=""
            if col:
                for para in self.block[col]:
                    paras+=para
                self.all_content['body'].append(paras)
        self.all_content['specific_table']=self.foot_table
        self.all_content['normal_table']=self.table


def main():
    '''initial search'''
    head='https://zh.wikipedia.org/w/index.php?'
    tail='&title=Special%3A%E6%90%9C%E7%B4%A2&go=%E5%89%8D%E5%BE%80'
    # input_str=input('输入查询词：')
    ser_list=[]
    with open('start','rb') as f_open:
        START_WORD=f_open.read().decode('utf-8').strip()
    with open('face rec.txt','r',encoding='utf-8') as f_open:
         every=f_open.readlines()
    ser_list=[i.strip() for i in every]
    log_file=logging_module.MyLog('log.txt')
    itero=0
    flag=True
    print(START_WORD)
    if START_WORD=='':
        flag=False
    for name in ser_list: 
        itero+=1 
        if flag:
            flag=(name!=START_WORD)
            continue
        if itero%10==0:
            time.sleep(20)
        if itero%30==0:
            write_StartWord(ser_list[itero-2])     
        search=urllib.parse.quote(name)
        url=head+search+tail
        value={'search': name,'title': 'Special:搜索','go': '前往'}
        # data=urllib.urlencode(calue)
        data=urllib.parse.urlencode(value).encode('utf-8')
        cut='https://zh.wikipedia.org/'
        '''get status code'''
        res=getStatusCode(url,data)
        # res=getStatusCode(url)
        if res.code==200:
            log_file.info('无 %s 词条'%name)
            req=res.read().decode('utf-8')
            soup=BeautifulSoup(req,'html.parser')
            try:
                extends=process_nonRes_words(soup)
                dict_out={'extendWords':extends}
                with open('non-res/%s.json'%name,'w+',encoding='utf-8') as f_write:
                    json.dump(dict_out,f_write,ensure_ascii=False)
            except:
                pass
            # return
            continue
        elif res.code==302:
            try:
                los=res.getheader(name='Location')
                los=cut+'zh-cn/'+re.split('/',los)[-1]
                soup=get_wiki_page(los)
            except Exception as erro:
                log_file.error('%s: %s'%(name,erro))
                # return
                continue
            if resOrDisambi(soup):
                # print("有以下多义的词条")
                items,href=process_ambig_words(soup)
                dict_ambig={'ambig_words':items}
                with open('ambig-res/%s.json'%name,'w+',encoding='utf-8') as f_write:
                    json.dump(dict_ambig,f_write,ensure_ascii=False)
                # flag=True
                # while(flag):
                #     try:
                #         input_n=input('请输入对应的序号:')
                #         los=href[int(input_n)]
                #         los=cut+'zh-cn/'+re.split('/',los)[-1]
                #         flag=False
                #     except:
                #         print('输入序号错误，请重试')
                # try:
                #     soup=get_wiki_page(los)
                # except Exception as erro:
                #     print(erro)
                #     return
                for item in href:
                    los=cut+'zh-cn/'+re.split('/',item)[-1]
                    try:
                        soup=get_wiki_page(los)
                        test=WikiNormal(soup)
                        title=test.head
                        with open('normal-res/%s.json'%title,'w+',encoding='utf-8') as f_write:
                            json.dump(test.all_content,f_write,ensure_ascii=False)
                    except:
                        pass
                log_file.warn('%s 为多义词'%name)
            else:
                pass 
        '''process a source page as wiki class'''
        try:        
            test=WikiNormal(soup)
            with open('normal-res/%s.json'%name,'w+',encoding='utf-8') as f_write:
                json.dump(test.all_content,f_write,ensure_ascii=False) 
        except Exception as erro:
            log_file.error('%s: %s'%(name,erro))
            continue
    # print(test.head)
    # print(test.abstract)
    # print(test.cols)
    # print(test.block)
    # print(test.block[test.cols[0]])
    # print(test.foot_table)
    # print(test.table)
    # print(test.all_content)

def write_StartWord(word):
    with open('start','wb') as f_write:
        f_write.write(word.encode('utf-8')) 

if __name__ == '__main__':
    main()