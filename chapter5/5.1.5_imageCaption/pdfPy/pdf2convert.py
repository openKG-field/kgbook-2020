# -*- coding: utf-8 -*-
"""
"""
import glob
import fitz
import os
from PIL import Image
#import matplotlib.pyplot as plt
from pdfread import imgRecogByPixMap
from pymongo import MongoClient

def mqpatMongo(tb):
    host = '10.0.4.2'
    port = 27017
    passwd = '123456'
    dbName = 'mqpat'
    user = 'mqpat-rw'
    myTbNme = tb
    conn = MongoClient(host,port)
    db = conn[dbName]
    db.authenticate(user, passwd)
    collection = db[myTbNme]
    return (conn,db,collection) 

(conn,db,col) = mqpatMongo('pdfDoneList')

def rightinput(desc):
    flag=True
    while(flag):
        instr = input(desc)
        try:
            intnum = eval(instr)
            if type(intnum)==int:
                flag = False
        except:
            print('请输入正整数！')
            pass
    return intnum


# def mkdir(path):
#     # 去除首位空格
#     path = path.strip()
#     # 去除尾部 \ 符号
#     path = path.rstrip("\\")
#     isExists = os.path.exists(path)
#     # 判断结果
#     if not isExists:
#         os.makedirs(path)
#         return True
#     else:
#         # 如果目录存在则不创建，并提示目录已存在
#         print
#         path + ' 目录已存在'
#         return False
def outImg(img,out,count):
    img.save(out+str(count) + '.jpg')
    return 0 
    
    
def pdf2png(name,file):
    pdffile = glob.glob(name)[0]
    if not os.path.exists(file.replace('.pdf','')):
        os.mkdir(file.replace('.pdf',''))
        
        
    outputDir = ''
        
    outputDir = outputDir + '/'
    doc = fitz.open(pdffile)
    flag = 1
    if flag == 1:
        strat = 0
        totaling = doc.pageCount
    else:
        strat = rightinput('输入起始页面：') - 1
        totaling = rightinput('输入结束页面：')
    count = 0
    bg = False
    for pg in range(strat, totaling):
        count += 1
        page = doc[pg]
        zoom = int(100)
        rotate = int(0)
        trans = fitz.Matrix(zoom / 50.0, zoom / 50.0).preRotate(rotate)
        pix = page.getPixmap(matrix=trans, alpha=False)
        rgb = "RGB"                       # set PIL parameter
        if pix.alpha:                     # JPEG cannot have alpha!
            pix0 = fitz.Pixmap(pix, 0)    # drop alpha channel
            pix = pix0                    # rename pixmap
        img = Image.frombuffer(rgb, [pix.width, pix.height], pix.samples,
                       "raw", rgb, 0, 1)
        if count > 3 :
            
            jg = imgRecogByPixMap(img,'CN')
            #jg = True
            if bg or jg :
                bg = True
                outImg(img, outputDir,count)
           	#print outputDir, count 
                #plt.figure('show')
                #plt.imshow(img)
                #plt.show()
        continue 


        
        # os.rename(spath,spath)
        #os.mkdir(name.rstrip('.pdf'))
       
        
        #os.makedirs(path)
        #isExists\
        # os.mkdir('\\'+name.rstrip('.pdf'))
        # currentpath = os.getcwd()
        # print
        # "currentpath: ", currentpath
        # if not isExists:
        #     src = os.mkdir(name.rstrip('.pdf')).format(path)
        # else:
        #     pass
        #os.chdir()
        #print (src)
        #pm.writePNG('%s.png' % str(pg+1))
        #print outputDir
#         if pg+1 < 10:
#             pm.writePNG('%s\\%s.png' % (outputDir,'0'+str(pg+1)))
#         else:
#             pm.writePNG('%s\\%s.png' % (outputDir,str(pg+1)))
def sortfile(l):
    for i in range(len(l)):
        l[i] = l[i].split('.')
        l[i][0] = int(l[i][0][8:])
    l.sort()
    for i in range(len(l)):
        l[i][0] = str(l[i][0])
        l[i] = "pic2pdf\\"+l[i][0] + '.' + l[i][1]
    return l
def spend(time):
    m, s = divmod(time, 60)
    h, m = divmod(m, 60)
    print ("%02d:%02d:%02d" % (h, m, s))

def mongoExists(pubid):
    for data in col.find({'pubid':pubid}).limit(1):
        return True
    return False
    
    
    
import os
import time
if __name__ == '__main__':
    s = time.time()
    count  = 0
    inputPath = ''
    name = 't.pdf'
    file = 't.pdf'
    pdf2png(name,file)
        #    if count % 30 is 0 :
        #        break
	#if count % 30 is 0 :
	#    break
    e = time.time()
    spend(e-s)
#     name = 'CN1179250A.pdf'
#     file = 'CN1179250A.pdf'
#     pdf2png(name, file)
    # pic2pdf()
    # pdf2word(name)
    
'''
<class 'fitz.fitz.Pixmap'>
<class 'PIL.Image.Image'>


'''
