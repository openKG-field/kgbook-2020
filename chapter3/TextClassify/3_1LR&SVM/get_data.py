#coding=utf8
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

from mongoC import mongC

(conn,db,col) = mongC.mqpatMongo('signClaimsList')


wanted = {'manpowerLabel':1,'pubid':1,'_id':0}

# wanted = {''}

f = open(r'./data/noman_feautures.txt','w')

pubids = {}

break_flag = '$$$$'
for data in col.find({'userid':'gongniu2'},wanted).batch_size(100):
    tem = ['_'.join(data['manpowerLabel']['product']) , \
           '_'.join(data['manpowerLabel']['firstFeature']) ,\
           '_'.join(data['manpowerLabel']['secondFeature']) ,\
           '_'.join(data['manpowerLabel']['thirdFeature']) ,\
           '_'.join(data['manpowerLabel']['fourthFeature']) ]
    features = ','.join(tem)
    pubid = data['pubid']
    pubids[pubid] = {'feauture':features}
    #f.write(pubid +break_flag + feautres + '\n')
    
    
(conn,db,col) = mongC.mqpatMongo('threatPatentMark')

print (col.count({'userid':'gongniu2'}))

for data in col.find({'userid':'gongniu2'},{'_id':0,'pubid':1,'fieldsName':1,'fieldWords':1,'techWords':1,'funcWords':1,'tfidf_v1':1,\
                                            'goodsList':1,'warnLevelRe':1,'indLen':1,'claimsIndCount':1,'mainIpc3':1}).batch_size(100):
    
    pubid = data['pubid']
    if pubid in pubids :
        data.pop('pubid')
        #print(data)
        if 'goodsList' in data:
            data['goodsList'] = ','.join(data['goodsList'])
        if 'tfidf_v1' in data and type(data['tfidf_v1']) is list:
            data['tfidf_v1'] = ','.join(data['tfidf_v1'])
        pubids[pubid].update(data)
    else:
        data.pop('pubid')
        if 'goodsList' in data:
            data['goodsList'] = ','.join(data['goodsList'])
        if 'tfidf_v1' in data and type(data['tfidf_v1']) is list:
            data['tfidf_v1'] = ','.join(data['tfidf_v1'])
        pubids[pubid] = data
        data['feature'] = 'None_value'
        
        #print(pubids[pubid])
        #break

keys = ['pubid','fieldsName','fieldWords','techWords','funcWords','tfidf_v1','goodsList','warnlevelRe','indLen','claimsIndCount','feature','mainIpc3']

f.write(break_flag.join(keys) + '\n')

for pubid in pubids:
    data = pubids[pubid]
    tem = [pubid]
    for k in keys:
        if k =='pubid' : continue
        if k not in data :
            tem.append('None_Value')
        else:
            #if type(data[k]) is list:
            #    print(k)
            tem.append(str(data[k]))
    
    f.write(break_flag.join(tem) + '\n')

    
    

    

if __name__ == '__main__':
    pass