#coding=utf-8
'''
Created on 2018��8��21��

@author: wangn
'''
import pytesseract
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
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

def imageDetermine(path,country):
    
    global count
    org = Image.open(path)
    
    img = np.array(Image.open(path).convert('1'))
    
    
    
    (x,y) = img.shape
    
#     subImg = img[:x/5]
#     plt.figure('sub')
#     plt.imshow(subImg)
#     plt.show()
    
    box = (1,1,y-1,x/10)
    
    if country == 'CN':
        head = org.crop(box)
        #
        plt.imshow(head)
        plt.show()
        
        a  = pytesseract.image_to_string(head,lang='chi_sim')
        
        a = a.replace(' ','').replace('\n','').replace('_','')
        

        if '说明书附图' in a.encode('utf-8') or '房色日月书阡寸图' in a.encode('utf-8') or '说日月书阡寸图' in a.encode('utf-8') or '说明书阡寸图' in a.encode('utf-8'):
            org.save('./pdf/'+str(count)+'.jpg')
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

            if float(len(a))/float(height) < 0.35 :
                sub.save('./pdf/'+str(count)+'.jpg')
                count += 1
                
    #imageDetermine(path)
import os

def getPaths(path):
    count = 0 
    for root,dirs,files in os.walk(path):
        for file in files:
            p = os.path.join(root,file)

            count += 1
            #print count
    
#path = 'page-4.jpg'
#getPaths(path)   
path = 'C:\\Users\\zhaoh\\eclipse-workspace\\CNENSep\\Pdfreader\\page-7.png'
country = 'CN'
imageDetermine(path, country)   

    
    

 