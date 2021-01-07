#coding=utf-8
'''
Created on 2018��8��21��

@author: wangn
'''
import pytesseract
from PIL import Image

import numpy as np
#import matplotlib.pyplot as plt
path = u'D:\\LDA\\protege\\Pdfreader\\image\\test3.jpg'

count = 0 

def imageCatch(img):
    imgs = []
    (a,b) = img.shape
    line = a/100
    head= -1
    bottom = -1
    height = b/5
    begin = 0
    while begin < a :
        tem = img[begin:begin+line]
        if tem.mean() == 1.0:
            if head != -1 :
                bottom = begin
            else:
                head = begin
            
            if bottom - head < height:
                head = begin
            else:
                
                imgs.append((1,head,b-1,bottom))
                
                head = bottom
        begin = begin + line 
    return imgs  

def imgRecogByPixMap(org,country):
    #root = root.replace('pdfTest','image')
    img = np.array(org.convert('1'))
    
    
    
    (x,y) = img.shape
    
#     subImg = img[:x/5]
#     plt.figure('sub')
#     plt.imshow(subImg)
#     plt.show()
    #box is use to cut the head of fig with left right high and bottom index
    box = (1,3,y-1,x/5)
    #when input image come from a cn patent
    if country == 'CN':
        head = org.crop(box)
        #print type(head)
        #plt.imshow(head)
        #plt.show()
        #apply a word recognize function 
        #tessdata_dir_config = '--tessdata-dir "C:\\Python27\\Lib\\site-packages\\pytesser\\tessdata"'
        a  = pytesseract.image_to_string(head,lang='chi_sim')
        
        a = a.replace(' ','').replace('\n','').replace('_','')
        
        #print 'read word = ',a
        #if the a contains a list of words which can be recognized by pytesser, we assume the image is the fig of current patent
        #if '说明书附图' in a.encode('utf-8') or '房色日月书阡寸图' in a.encode('utf-8') or '说日月书阡寸图' in a.encode('utf-8') or 'i兑日月书网寸冬' in a.encode('utf-8')or '说明书阡寸图' in a.encode('utf-8'):
	if ('日'in a.encode('utf-8') and  '月' in a.encode('utf-8') and '图'in a.encode('utf-8')) or '附图' in a.encode('utf-8') or '说明书附图' in a.encode('utf-8') or '房色日月书阡寸图' in a.encode('utf-8') or '说日月书阡寸图' in a.encode('utf-8') or 'i兑日月书网寸冬' in a.encode('utf-8')or '说明书阡寸图' in a.encode('utf-8') :       
    
            #count += 1
            return True

def imageDetermine(root,path,country):
    
    global count
    #count = 0 
    org = Image.open(path)
    #root = root.replace('pdfTest','image')
    img = np.array(Image.open(path).convert('1'))
    
    
    
    (x,y) = img.shape
    
#     subImg = img[:x/5]
#     plt.figure('sub')
#     plt.imshow(subImg)
#     plt.show()
    #box is use to cut the head of fig with left right high and bottom index
    box = (1,3,y-1,x/5)
    #when input image come from a cn patent
    if country == 'CN':
        head = org.crop(box)
        print type(head)
        #plt.imshow(head)
        #plt.show()
        #apply a word recognize function 
        tessdata_dir_config = '--tessdata-dir "C:\\Python27\\Lib\\site-packages\\pytesser\\tessdata"'
        a  = pytesseract.image_to_string(head,lang='chi_sim',config=tessdata_dir_config)
        
        a = a.replace(' ','').replace('\n','').replace('_','')
        
        #print a
        #if the a contains a list of words which can be recognized by pytesser, we assume the image is the fig of current patent
        if '说明书附图' in a.encode('utf-8') or '房色日月书阡寸图' in a.encode('utf-8') or '说日月书阡寸图' in a.encode('utf-8') or 'i兑日月书网寸冬' in a.encode('utf-8')or '说明书阡寸图' in a.encode('utf-8'):
            #org.save(root.replace('pdfTests','image') + '\\'+str(count)+'.jpg')
            count += 1
            return True
    
    if country == 'US':
        imgs = imageCatch(img)
        for i in imgs:
            sub = org.crop(i)
            (left,top,right,bottom) = i
            height = bottom - top
            a  = pytesseract.image_to_string(sub,lang='chi_sim')
            a = a.replace(' ','').replace('\n','').replace('_','')
#             print a 
#             if '发明专利申请' in a.encode('utf-8') or '中华人民共和国国家知识产权局' in a.encode('utf-8') or '申请公布号' in a.encode('utf-8'):
#                 continue
#             
#             if '说明书附图' in a.encode('utf-8'):
#                 sub.save('./pdf/'+str(count)+'.jpg')
#                 count += 1
#                 continue
        #   print len(a)
        #print height
            #print count , float(len(a))/float(height)
            if float(len(a))/float(height) < 0.35 :
                sub.save('./pdf/'+str(count)+'.jpg')
                count += 1
                
    #imageDetermine(path)
import os
import json
def getPaths(path):
    #the final output image path list txt file
    
    o = open('D:\\image\\figPath.txt','w')
    dirCount  = 0 
    for root,dirs,files in os.walk(path):
        dirCount  += 1
        if 'CN' not in root :
            continue
        #if dirCount > 3 :
        #    break
        figList = []
        #print root
        # for each CN image file, read each of the image and recognize if the image is the fig of description and out the path in o file
        imgCount = 0
        bg = False
        for file in files:
            #print root
            imgCount += 1
            if imgCount < 4 :
                continue
            #skip the 1st, 2nd and 3rd figs ,cuz they can not be the part of description
            p = os.path.join(root,file)
            
            # find the first fig of description and we assume the figs which comes from the 1st one will always be fig of description
            if not bg: 
                #imageDetermin function is a boolean function which will determine if the current image is the fig of patent's description
                print 'p = ',p
                if  imageDetermine(root,p,'CN'):
                    bg = True
                    figList.append(p)
            else:
                figList.append(p)
        # keep all paths in figList and apply json.dumps into o file with '\n' in the end of line
    
        o.write(json.dumps(figList)+'\n')

#path is the input path which store the all pdf images file             


    
    

 
