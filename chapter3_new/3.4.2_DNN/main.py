#coding='utf8'

'''
run test for rcnn and textcnn
'''

from rcnn import rcnn
from textcnn import textcnn

def load_data(train_path,test_path):
    head = 'type,tfidf_cnt,tfidf&tar_cnt,tech_cnt,tech&tar_cnt,agentList_cnt,problem_cnt,problem&tar_cnt,func_cnt,func&tar_cnt,applicantFirst,target'.split(',')

    train_data_pd = pd.read_csv(train_path, sep=',', header=0, encoding='utf8')
    test_data_pd = pd.read_csv(test_path, sep=',', header=0, encoding='utf8')

    x_train = train_data_pd[head[:-2]]
    y_train = train_data_pd[head[-1]]

    print(x_train)
    x_test = test_data_pd[head[:-2]]
    y_test = test_data_pd[head[-1]]


    rc= rcnn(input_dim=len(head[:-2]),dnn_unit=16)
    rc.build({'Q': x_train, 'C': x_train}, y_train, [x_test, x_test], y_test, batch_size=50, epochs=100)
    
    
    tc= textcnn(input_dim=len(head[:-2]),dnn_unit=16)
    tc.build({'Q': x_train, 'C': x_train}, y_train, [x_test, x_test], y_test, batch_size=50, epochs=100)
    
    
    #wd.build({'lr':x_train,'dnn':x_train},y_train,[x_test,x_test],y_test,batch_size=50,epochs=100)


train_path = '.\\..\\..\\data\\train_data.txt'
test_path =  '.\\..\\..\\data\\test_data.txt'

load_data(train_path,test_path)