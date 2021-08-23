# coding:utf-8

import json
import requests
import execjs
import sys

if sys.version_info[0] == 2:  # Python 2
    from urllib import quote
else:  # Python 3
    from urllib.parse import quote
import locale

locale.getdefaultlocale()[1]


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072; 
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f"; 

 
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 

            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 

    }; 

 

    function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
    } 

    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)



def translate(content):
    try:
        if len(content) == 0:
            texts = ''
            return texts
        js = Py4Js()
        tk = js.getTk(content)
        content = quote(content)
        url = "请输入你申请的google翻译的url" % (tk, content)
        response = requests.get(url)
        result = response.content
        item = json.loads(result)
        texts = ""
        for i in range(0, len(item[0])):
            if str(item[0][i][0])!="None":
                texts += str(item[0][i][0])
        return texts
    except:
          return ""

# 将英文翻译成中文
def zh(content):
    texts = ""
    try:
        if len(content) == 0:
            return texts
        js = Py4Js()
        tk = js.getTk(content)
        content = quote(content)
        url = "请输入你申请的google翻译的url" % (tk, content)
        response = requests.get(url)
        result = response.content
        #print 'result = ',result
        item = json.loads(result)
        #print len(item[0])
        for i in range(len(item[0])):
            
            if item[0][i][0] is not None:
                #print i,item[0][i][0], [item[0][i][0]]
                texts += item[0][i][0]
        return texts
    except:
        print ('error happen')
        return ""

def split_string(str,cutting_method):
    item = str.split(cutting_method)
    interception_len = len(item)/2
    interception1 = ".".join(item[:interception_len])
    interception2 = ".".join(item[interception_len:len(item)])
    return interception1,interception2

def get_string(str,cutting_method):
    list = []
    interception1,interception2 = split_string(str,cutting_method)
    if len(interception1) > 5000:
        list1 = get_string(interception1,cutting_method)
        list = list+list1
    else:
        list.append(interception1)
    if len(interception2) >5000:
        list1 =get_string(interception2,cutting_method)
        list = list + list1
    else:
        list.append(interception2)
    return list

# 自动检测语言后翻译成英文
def get_translate(context):
    str =""
    if len(context) > 50000:
        list = get_string(context,".")
        count = 0
        for item in list:
            count+=1
            if count != len(list):
                item =item+"."
            str+=translate(item)
        print (count)
    else:
        str = translate(context)
    return str

#英文翻译中文
def get_zh(context):
    str =""
    if len(context) > 5000:
        list = get_string(context,".")
        count = 0
        for item in list:
            count+=1
            if count != len(list):
                item =item+"."
            str+=zh(item)
            print (str)
    else:
        trans = zh(context)
        #print 'trans = ',trans
    return trans
import json
if __name__ == '__main__':

    try:
        input  = '''
        execjs适合在有完整的js function代码的情况下使用。

示例代码的场景是，爬取的邮箱地址是经过加密的，但能够在js代码里面找到解密的代码，就是下面的js_code，接下来需要把加密邮箱用解密代码解出真正的邮箱。

通过执行js_code里的decryptString函数来解密邮箱地址，decryptCharcode函数会被decryptString函数调用，所以需要保留。
        '''

        count = 0
        #tem.truncate()
        for line in input.split():
            count +=1
            #调用google翻译，自动识别英译中|中译英
            result = get_translate(line)

            print(result)

    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        json.dump({'key':count},open('continue.json','w'))




