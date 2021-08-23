集成了Logistic Regression模型、线性分类模型。TODO:补充最大熵分类项目。
对同一组数据的对比结果如下：

C:\Python36\python.exe D:/NLPdeepLearning/kgbook-2021/kgbook-2020/chapter3/3.3.1_TextClassify/LR&SVM/LR&SVM&lineRe.py
C:\Python36\lib\site-packages\sklearn\ensemble\weight_boosting.py:29: DeprecationWarning: numpy.core.umath_tests is an internal NumPy module and should not be imported. It will be removed in a future NumPy release.
  from numpy.core.umath_tests import inner1d
15285    1
5412     0
16512    1
20598    1
23097    0
15954    0
712      1
15029    1
13612    1
14985    0
8388     1
7474     1
13848    1
18776    1
650      1
11193    1
26129    1
19033    0
13509    1
14187    1
808      1
12661    1
12564    1
18085    1
19905    1
23152    0
5575     1
3915     0
11425    1
14667    1
        ..
15040    1
1594     1
4541     1
14210    0
580      1
12100    0
25101    1
8317     1
17449    1
25693    1
5004     1
25773    0
19505    0
15502    1
8539     1
15984    1
16395    1
25377    0
10566    0
3256     1
21476    0
5762     1
19855    1
7128     0
18676    1
25433    1
14030    1
22683    1
4951     1
12772    1
Name: target, Length: 6617, dtype: int64
[4797] [6248]
[4797] [4958] recall true binary ('f-score',)
[4797] [4958]
0.9675272287212586
[4797] [6248]
[4797] [4958] recall true binary ('recall',)
[4797] [4958]
0.9675272287212586

        evluation of SVM_model is :
        f1_score = 0.8561484918793504
        accuracy = 0.756385068762279
        recall = 0.9675272287212586
        log_loss = 8.41433697513484
        auc = 0.5464519808464642
    
[4899] [6508]
[4899] [4958] recall true binary ('f-score',)
[4899] [4958]
0.9881000403388464
[4899] [6508]
[4899] [4958] recall true binary ('recall',)
[4899] [4958]
0.9881000403388464

        evluation of LR_model is :
        f1_score = 0.8545264259549974
        accuracy = 0.7479220190418618
        recall = 0.9881000403388464
        log_loss = 8.706659449747047
        auc = 0.5091193390362103
    
[1 1 1 ... 1 1 1]
[4925] [6552]
[4925] [4958] recall true binary ('f-score',)
[4925] [4958]
0.9933440903590157
[4925] [6552]
[4925] [4958] recall true binary ('recall',)
[4925] [4958]
0.9933440903590157

        evluation of line is :
        f1_score = 0.8557775847089487
        accuracy = 0.7491310261447786
        recall = 0.9933440903590157
        log_loss = 8.664903998877234
        auc = 0.5063164092542517
    

Process finished with exit code 0
