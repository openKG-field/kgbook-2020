#coding=utf-8


from pdf2image import convert_from_path
import tempfile
pdffilename = "CN1038012C.pdf"


#a = open('/mnt/d/LDA/protege/Pdfreader/test.txt','r')
#
#for line in a :
#    print line



#pdf_im = PdfFileReader(pdffilename)
#image = convert_from_path("CN1038012C.pdf")

#npage = pdf_im.getNumPages()

#print('Converting %d pages.' % npage)
#a = open('test.txt','r')
outputDir = './images/'

with tempfile.TemporaryDirectory() as path:

    images = convert_from_path(pdffilename)
    for index, img in enumerate(images):
        img.save('%s/page_%s.png' % (outputDir, index))


    # print pdffilename + '[' + str(p) +']','file_out-' + str(p)+ '.png'
