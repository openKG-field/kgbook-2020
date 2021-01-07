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
        url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&ssel=3&tsel=0&kc=0&tk=%s&q=%s" % (
        tk, content)
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
        url = "https://translate.google.cn/translate_a/single?client=t&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&pc=1&otf=1&ssel=0&tsel=0&kc=1&tk=%s&q=%s" % (
        tk, content)
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
        print 'error happen'
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
        print count
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
            print str
    else:
        trans = zh(context)
        #print 'trans = ',trans
    return trans
import json
if __name__ == '__main__':
    source = 'inputRaw.txt'
    count = 0
    target = 'T_' + source
    temFile = 'tem_'+source
    errorCount = 0
    try :
        errorCount = json.load(open('continue.json','r'))['key']
    except :
        pass
    print 'already finished ',errorCount
    try:
        chinese = open(source, 'rt')
        f = open(target,'a')

        #tem.truncate()
        for line in chinese.readlines():
            count +=1
            if count < errorCount:
                continue
            print count

            result = get_translate(line)
            print 'result = ', result
            f.write(result+'\n')
            f.flush()
        f.close()

    except Exception as ex:
        print('[-]ERROR: ' + str(ex))
        json.dump({'key':count},open('continue.json','w'))

        #return
    # result = get_translate("一种采用丝网印刷方式制备的薄膜开关及制备装置和方法 \\"
    #                        "一种安全头盔"
    #                        "本发明提供一种安全头盔，其包括核心处理芯片、信号发生器、信号采集器、工作模式转换器、报警模块和电源模块。使用者将安全"
    #                        "盔调至工作模式之后，信号发生器不断地发出探测信号并返回信号至信号采集器，信号采集器简单处理之后再发动给核心处理芯片，"
    #                        "核心处理芯片做具体的分析处理判断，确定是否触发报警装置，从而使人们能提前避险。"
    #                        "防雾霾头盔"
    #                        "本发明公开了一种防雾霾头盔，包含一帽体，所述的帽体的下边缘设有一护围，所述的帽体上可活动地设有一面罩，所述的面罩上设"
    #                        "一挡风眼镜。")
    # print 'result = ',result


