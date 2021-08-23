import json,re,os,time
from pyltp import Segmentor

LTP_DATA_DIR =('../ltp-model/')
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
segmentor = Segmentor()
segmentor.load(cws_model_path)

import xmlrpc.client as xc
proxy =xc.ServerProxy("http://103.31.53.213:30003")

def extractBracket(words):
    words=re.sub('（|）','',words)
    return re.split('：|，|,',words)

def elitSimpleFormat(sentence):
    sents=re.split(r"([（(][a-z,A-Z,\s,(缩写)]*?[）)])",sentence)
    if len(sents)==1:return 0,0
    s=map(lambda k,v:(k,v),sents[::2],sents[1::2])
    howTo={k:v for k,v in s}
    end=sents[-1]
    return howTo,end

def bracketDetector(sentences):
    howTo={}    
    for sentence in sentences:
        sents=re.split(r"([（(]英语[：:].*?[）)])",sentence) 
        s=map(lambda k,v:(k,v),sents[::2],sents[1::2])
        for k,v in s:
            append,end=elitSimpleFormat(k)
            if not append:
                howTo[k]=v
                continue
            for k_a,v_a in append.items():
                howTo[k_a]=v_a
            howTo[end]=v
        append,end=elitSimpleFormat(sents[-1])
        if append:
            for k_a,v_a in append.items():
                howTo[k_a]=v_a
    return howTo

def connect_ch(ch,en):
    seg=list(segmentor.segment(k))
    uy=""
    use=len(en.split())
    if len(seg)<=use: return ch,ch
    uyp1=seg[-(use+1)]
    for i in range(use)[::-1]:
        uy+=seg[-(i+1)]
    return uy.strip(),(uyp1+uy).strip()

def connect_cn_jieba_all(ch,en):
    ch=re.findall('(\w+)\W?$',ch.strip())[-1]
    seg=list(proxy.jiebaWords(ch))
    res=list(map(lambda x:re.split('_*_',x),seg))[::-1]
    use=(len(en.split()))
    uy="";out=""
    for i in res:
        if i[2] not in ['n','b','c','x','vn','nr']:
            break
        out=i[0]+out
    if len(seg)<=use:return ch,ch,out
    uyp1=re.split('_*_',seg[-(use+1)])[0]
    for i in range(use)[::-1]:
        uy+=re.split('_*_',seg[-(i+1)])[0]
    if (not out) :out=uy.strip()
    return [uy.strip(),(uyp1+uy).strip(),out]

def build(x, y):
    return lambda: x * x + y * y

# f=open('wiki-ex-full.txt','r',encoding='utf-8')
st3="";set_v="";set_j=""
head='./wiki-full-context/context/'
for i in os.listdir(head)[2:]:
    li=os.listdir(head+i)
    if i=='AC':li=li[17:]
    for j in li:
        print(j)
        with open(head+i+'/'+j,'r',encoding='utf-8') as f_r:
            for index, line in enumerate(f_r.readlines()):
                if i=='AC' and li == li[0] and index<65:continue
                if index%400==0:time.sleep(2)
                # elitSimpleFormat(json.loads(f.readline())['text'])
                jo=json.loads(line.strip())['text']
#                 extends=jo['text']
                # print(jo)
                # for key,val in dict(jo).items():
                # print(jo)
                # bracketDetector(segmentor(jo))
                weigtsed=bracketDetector([jo])
                # print(weigtsed)
                for k,v in weigtsed.items():
                    if len(k.strip())==0 or len(v.strip())==0:continue
                    vs=extractBracket(v)
                    if vs[0]=='英语':
                        set_v=vs[1]
                        set_j=vs[2:]
                    else:
                        set_v=vs[0]
                        set_j=vs[1:]
                    try:
                        k=k.split()[-1]
                        k=re.split(r'\\n',k)[-1]
                        st0=re.sub('\W','',k)
                        st1,st2,st3=connect_cn_jieba_all(k,set_v)
                        if not st3:st3=st1
                        if len(st3)<=1:st3=st2
                        print(st1,st2,st3,set_v)    
                        out={"中文名":st3,"外文名":set_v,"解释":set_j}
                        a = json.dumps(out)
                        with open('new3.txt','a') as f_a:
                            f_a.writelines(a+'\n')
            #             f_a.writelines(a+'\n')
                    except:print(i) 
# f.close()