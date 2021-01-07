#encoding=utf-8
'''
Created on 2017年12月13日

@author: zhaoh
'''

import xmlrpclib
import time
proxy = xmlrpclib.ServerProxy("http://172.10.30.41:30010")
start = time.time() 
k = 5
t = 10
userid = 'wangyuxiu'
result = proxy.clusterPattern(k,t,userid)


#('分类' or '分选' or '种类' or '分拣' or '光谱') and ('木材' or '木板' or '木头' or '木块' or '实木' or '原木')

end = time.time()

