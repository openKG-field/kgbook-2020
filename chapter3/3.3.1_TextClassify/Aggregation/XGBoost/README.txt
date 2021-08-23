xgb.py

xgb模型效果展示
data为本书标准数据
config中包含部分xgb调用参数，具体调节可参考书中内容
使用时，注意xgb模型包本身的安装

params = {
    'booster': 'gbtree',   #弱分类器
    'objective': 'multi:softmax',   #分类方式
    'num_class':2, #分类器数量
    'max_depth': 5,  #最大深度
    'subsample': 0.7, #子采样比例
    'colsample_bytree': 0.7, #列采样利弊
    'min_child_weight': 3, #最小权重

}
结果展示
D:\Anconda\python.exe D:/NLPPractice/kgbook-2020/kgbook-2020/chapter3_new/3.3.1_TextClassify/Aggregation/XGBoost/xgb.py
D:\Anconda\lib\site-packages\numpy\_distributor_init.py:32: UserWarning: loaded more than 1 DLL from .libs:
D:\Anconda\lib\site-packages\numpy\.libs\libopenblas.IPBC74C7KURV7CB2PKT5Z5FNR3SIBV4J.gfortran-win_amd64.dll
D:\Anconda\lib\site-packages\numpy\.libs\libopenblas.PYQHXLVVQ7VESDPUVUADXEVJOBGHJPAY.gfortran-win_amd64.dll
  stacklevel=1)
.\..\..\..\data\train_data.txt
sep =  ,
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 21998 entries, 0 to 21997
Data columns (total 10 columns):
 #   Column           Non-Null Count  Dtype
---  ------           --------------  -----
 0   type             21998 non-null  int64
 1   tfidf_cnt        21998 non-null  int64
 2   tfidf&tar_cnt    21998 non-null  int64
 3   tech_cnt         21998 non-null  int64
 4   tech&tar_cnt     21998 non-null  int64
 5   agentList_cnt    21998 non-null  int64
 6   problem_cnt      21998 non-null  int64
 7   problem&tar_cnt  21998 non-null  int64
 8   func_cnt         21998 non-null  int64
 9   func&tar_cnt     21998 non-null  int64
dtypes: int64(10)
memory usage: 1.7 MB
None
{'booster': 'gbtree', 'objective': 'multi:softmax', 'num_class': 2, 'gamma': 0.1, 'max_depth': 5, 'lambda': 3, 'subsample': 0.7, 'colsample_bytree': 0.7, 'min_child_weight': 3, 'eta': 0.1, 'seed': 1000}
[0. 1. 1. ... 1. 1. 1.]

D:\Anconda\lib\site-packages\sklearn\metrics\_classification.py:2240: RuntimeWarning: divide by zero encountered in log
        evluation of xgb is :
        f1_score = 0.8757747933884298
  loss = -(transformed_labels * np.log(y_pred)).sum(axis=1)
        accuracy = 0.7847874720357941
D:\Anconda\lib\site-packages\sklearn\metrics\_classification.py:2240: RuntimeWarning: invalid value encountered in multiply
        recall = 0.9652718474238543
  loss = -(transformed_labels * np.log(y_pred)).sum(axis=1)
        log_loss = nan
        auc = 0.5437644503576952
    
xgboost  0.7847874720357941
0.12233422994613648 1623376567.3400538

Process finished with exit code 0