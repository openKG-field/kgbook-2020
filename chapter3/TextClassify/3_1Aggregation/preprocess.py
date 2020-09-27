#encodign=utf-8

import codecs
f = codecs.open('noman_feautures.txt','r',encoding='utf-8')
s = []
for i in f.readlines():

    s.append(i)

m = s[0].replace('$',' ').replace('    ','\t').replace('mainIpc3','apply_flag').split('\t')
ss=''
for i in m:
    i=i.strip()
    #covered_query_term_number
    ss = ss+'covered_query_term_number='+i+'\t'
print ('name:'+ss,type(ss))

ff =codecs.open('train_data','w',encoding='utf-8')
fff =codecs.open('test_data','w',encoding='utf-8')
for i in s[0:20000]:
    ff.write(' '.join(m for m in i.split('$$$$')).strip().replace(' ','\t').replace('    ','\t').replace('mainIpc3','apply_flag')+'\n')
ff.close()

for i in s[20001:]:
    fff.write(' '.join(m for m in i.split('$$$$')).strip().replace(' ','\t').replace('    ','\t').replace('mainIpc3','apply_flag')+'\n')
fff.close()