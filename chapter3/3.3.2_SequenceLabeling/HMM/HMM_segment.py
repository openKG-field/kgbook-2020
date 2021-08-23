# -*- encoding: utf-8 -*-
"""
@File    : HMM.py
@Time    : 2020/7/5 15:21
@Author  : Ryt_tech
@Email   : zhaohongyu2401@yeah.net
@Software: PyCharm
"""
import numpy as np
import os

class HMM():

    '''
    #Trans_matrix: A N个可能状态,N*N
    #Obs_matrix: B  M个可能观测状态,N*M
    #Initial_matrix: Pi 初始状态概率向量

    '''
    # states=
    # observations =
    # start_probability={}
    # transition_probability={}
    #
    # emission_probability={}

    #def dataSet(self):
    def __init__(self):
        self.states = ('人工','智能')
        self.obs_map = ('自动','高效','节省')
        self.initial_map ={'人工':0.8,'智能':0.2}
        self.trans_map = {
            '人工': {'人工': 0.7, '智能': 0.3},
            '智能': {'人工': 0.4, '智能': 0.6},
        }

        self.emission_map = {
            '人工': {'自动': 0.5, '高效': 0.4, '节省': 0.1},
            '智能': {'自动': 0.1, '高效': 0.3, '节省': 0.6},
        }

    # def __init__(self, A, B, pi):
    #     self.A = A
    #     self.B = B
    #     self.pi = pi

    #前向计算
    def _forward(self,obs_map):
        forward =[{}]
        #初始化时刻为t=0
        for i in self.states:
            forward[0][i] = self.initial_map[i]*self.emission_map[i][obs_map[0]]
            #print (forward[0][i])
            #t>0
        for t in range(1,len(obs_map)):
            forward.append({})
            for j in self.states:
                sum = 0.0
                for s0 in self.states:
                    #print (s0)
                    forward[t][j] = sum+(forward[t-1][s0]*self.trans_map[s0][j]*self.emission_map[j][obs_map[t]])
                #print (forward[t][j])
        sum =0.0
        for s in self.states:
            prob = sum+forward[len(obs_map)-1][s]
        return prob

    #后向计算
    def _backward(self,obs_map):
        backward =[{} for t in range(len(self.obs_map))]
        # from t= T时刻开始后向计算
        T = len(obs_map)
        for i in self.states:
            backward[T-1][i] = 1
        #print (backward)

        for t in reversed(range(T-1)):
            for i in self.states:
                #print (i)
                sum = 0.0
                for s0 in self.states:
                    backward[t][i] = sum + backward[t+1][s0] *self.trans_map[i][s0]*self.emission_map[s0][obs_map[t+1]]
        sum =0
        for i in self.states:
            prob = sum+self.initial_map[i]*self.emission_map[i][obs_map[0]]*backward[0][i]
        return prob

    #预测解码计算
    def _viterbi(self,obs_map):
        #states, initial_map, trans_map, emission_map
        #观测序列状态概率初始时刻t=0表示，
        delta =[{}]
        path={}
        for i in self.states:
            delta[0][i] = self.initial_map[i]*self.emission_map[i][obs_map[0]]
            path[i]=[i]
        for t in range(1,len(obs_map)):
            delta.append({})
            path_new={}


            #根据t-1时刻的状态概率、观测概率、状态转移概率计算下一时刻t的观测序列最大概率，计算最优路径
            for i in self.states:
                for j in self.states:
                    #print (type(delta[t-1][j]*self.trans_map[j][i]*self.emission_map[i][obs_map[t]]))
                    (prob,state) = max([(delta[t-1][j]*self.trans_map[j][i]*self.emission_map[i][obs_map[t]],j)])
                delta[t][i] = prob
                path_new[i] = path[state] + [i]
            path = path_new

        # 输出最优路径
        for i in self.states:
            (prob,state) = max([(delta[len(obs_map)-1][i],i)])
        return (prob,path[state])




    def _EM(self,obs_map,endpoint,pi):
        states_n = self.A.shape[0]
        samples_n = len(obs_map)

        flag = False
        while not flag:

            #计算某一时刻的前后向隐状态概率
            alpha = self._forward(obs_map)
            beta = self._backward(obs_map)

            #给定观测序列和HMM模型，t时刻和t+1时刻的隐状态概率phi,首先初始化phi
            phi = np.zeros((states_n,states_n,samples_n-1))
            #使用前后向算法计算状态转移概率矩阵A和观测概率矩阵B
            for t in range(samples_n - 1):
                denom = np.dot(np.dot(
                    alpha[:, t].T, self.A) * self.B[:, obs_map[t + 1]].T, beta[:, t + 1])
                for i in range(states_n):
                    numer = alpha[i, t] * self.A[i, :] * self.B[:,
                                                                obs_map[t + 1]].T * beta[:, t + 1].T
                    phi[i, :, t] = numer / denom
            # gamma_t(i) = P(q_t = S_i | O, hmm)
            gamma = np.squeeze(np.sum(phi, axis=1))
            # Need final gamma element for new B
            prod = (alpha[:, samples_n - 1] *
                    beta[:, samples_n - 1]).reshape((-1, 1))
            # append one more to gamma!!!
            gamma = np.hstack((gamma, prod / np.sum(prod)))

            newpi = gamma[:, 0]
            newA = np.sum(phi, 2) / \
                np.sum(gamma[:, :-1], axis=1).reshape((-1, 1))
            newB = np.copy(self.B)

            num_levels = self.B.shape[1]
            sumgamma = np.sum(gamma, axis=1)
            for lev in range(num_levels):
                mask = obs_map == lev
                newB[:, lev] = np.sum(gamma[:, mask], axis=1) / sumgamma

            if np.max(abs(self.pi - newpi)) < endpoint and \
                    np.max(abs(self.A - newA)) < endpoint and \
                    np.max(abs(self.B - newB)) < endpoint:
                done = 1

            self.A[:], self.B[:], self.pi[:] = newA, newB, newpi



#实例化HMM
hmm = HMM()
obs_map = ('自动','高效','节省')#self.obs_map
#前向后向计算对比
s = hmm._forward(obs_map = obs_map)
print(s)
ss = hmm._backward(obs_map=obs_map)
print (ss)

#viterbi解码结果显示
path = hmm._viterbi(obs_map=obs_map)
print (path)



