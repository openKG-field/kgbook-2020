# -*- encoding: utf-8 -*-
"""
@File    : pdf2image.py
@Time    : 2021/3/19 10:19
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""

import glob
import fitz
import os
from PIL import Image

from pdfread import imageDetermine




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


def outImg(img,out,count):
    img.save(out+str(count) + '.jpg')
    return 0 
    
    
def convert_from_path(name,file):
    '''
    :param name: 命名
    :param file: 文件名字|也是路径
    :return:
    '''
    pdffile = glob.glob(name)[0]
    #准备输入路径
    if not os.path.exists(file.replace('.pdf','')):
        os.mkdir(file.replace('.pdf',''))
        
    #输出文件的基础路径
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
        #图片预处理
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
            #针对中午识别出专利PDF中每页头部中文描述，确定当前页是否为图片页，可以调整为英文，只需要修改country=US
            jg = imageDetermine(img,'CN')
            #jg = True
            if bg or jg :
                bg = True
                outImg(img, outputDir,count)

        continue 

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

    
    
    
import os
import time
if __name__ == '__main__':
    s = time.time()
    count  = 0
    inputPath = ''
    name = 't.pdf'
    file = 't.pdf'
    pdf2png(name,file)

    e = time.time()
    spend(e-s)


    
