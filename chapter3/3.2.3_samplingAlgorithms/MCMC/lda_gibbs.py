#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@File     : gibbs.py
@Time     : 2021/6/21 19:42
@Author   : zhaohongyu
@Email    : zhaohongyu2401@yeah.net
@Software : PyCharm
"""


import numpy as np

#P(X1|X2)
def p_x_given_y(y, mus, sigmas):
    mu = mus[0] + sigmas[1, 0] / sigmas[0, 0] * (y - mus[1])
    sigma = sigmas[0, 0] - sigmas[1, 0] / sigmas[1, 1] * sigmas[1, 0]
    return np.random.normal(mu, sigma)

#P(X2|X1)_
def p_y_given_x(x, mus, sigmas):
    mu = mus[1] + sigmas[0, 1] / sigmas[1, 1] * (x - mus[0])
    sigma = sigmas[1, 1] - sigmas[0, 1] / sigmas[0, 0] * sigmas[0, 1]
    return np.random.normal(mu, sigma)


def gibbs_sampling(mus, sigmas,num=10 ,iter=int(5e3)):
    samples = np.zeros((iter, 2))
    # 初始化样本数据，默认数量为5000
    y = np.random.rand()
    print('init y = ',y)

    for i in range(iter):
        for j in range(num):
            x = p_x_given_y(y, mus, sigmas)
            y = p_y_given_x(x, mus, sigmas)
        samples[i, :] = [x, y]

    return samples



if __name__ == '__main__':
    mus = np.array([5, 5])

    sigmas = np.array([[1, .9], [.9, 1]])
    #设定二元正态分布
    print('mus and sigmas = ',mus,sigmas)
    samples = gibbs_sampling(mus, sigmas)
    print('after ',samples)

