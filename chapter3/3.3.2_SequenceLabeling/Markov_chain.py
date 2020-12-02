#coding=utf-8
import numpy as np
from matplotlib import pyplot
import sys

'''
以某X染色体的隐性疾病为例，有X，X；X x；x，x；三种可能性组合。
那么从某一时刻t开始，下一步t+1时刻的一阶马尔可夫链的状态转移矩阵可以获得，预测之后的状态情况。
比如X，x---》0.25*（X，X),0.5*(X,x),0.25*(x,x),系数表明转移概率。
'''
import os
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)
Trans_matrix=np.matrix([[1,0,0],
              [0.25,0.5,0.25],
              [0,0,1]
              ])

#初始状态为（X，X）
P = np.matrix([[0.5,0.5,0]])

plot_data=[]
for step in range(10):
    result=P*Trans_matrix**step
    plot_data.append(np.array(result).flatten())

# Convert the data format
plot_data = np.array(plot_data)

# 绘制图形
pyplot.figure(1)
pyplot.xlabel('Steps')
pyplot.ylabel('Probability')
lines = []
for i, shape in zip(range(6), ['r+', 'h', 'H']):
    line, = pyplot.plot(plot_data[:, i], shape, label="Status%i" % (i+1),scaley=[0,1])
    lines.append(line)
pyplot.legend(handles=lines, loc=5)
pyplot.savefig(os.path.join(curdir, "markov_predict_result.png"))