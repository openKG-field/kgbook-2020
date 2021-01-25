#encoding=utf-8
'''
'''


file = open('divideWordResult.txt','r')
result = open('result.txt','w')
count = 0
check = 100000
tem =''
for line in file:
    line = line.replace('\r','').replace('\n','')
    if line.isspace():
        continue
    head = line[:2]
    tem = line
    if head =='#!':
        count = count + 1
        if count%2 == 0:

            tem = '#&' + line[2:]
    result.write(tem)
    result.write('\n')
#     check -= 1
#     if check <0:
#         break
    
        