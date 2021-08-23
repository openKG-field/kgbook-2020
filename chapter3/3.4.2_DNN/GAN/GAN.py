import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from skimage.io import imsave
import os
import shutil



def build_generator(z_prior):
    w1 = tf.Variable(tf.truncated_normal([z_size,h1_size],stddev=0.1),name='g_w1',dtype=tf.float32)
    b1 = tf.Variable(tf.zeros([h1_size]),name='g_b1',dtype=tf.float32)
    h1 = tf.nn.relu(tf.matmul(z_prior,w1) + b1)
    w2 = tf.Variable(tf.truncated_normal([h1_size,h2_size],stddev=0.1),name='g_w2',dtype=tf.float32)
    b2 = tf.Variable(tf.zeros([h2_size]),name='g_b2',dtype=tf.float32)
    h2 = tf.nn.relu(tf.matmul(h1,w2)+b2)
    w3 = tf.Variable(tf.truncated_normal([h2_size,img_size],stddev=0.1),name='g_w3',dtype=tf.float32)
    b3 = tf.Variable(tf.zeros([img_size]),name='g_b3',dtype=tf.float32)
    h3 = tf.matmul(h2,w3)+b3
    x_generate = tf.nn.tanh(h3)
    g_params = [w1,b1,w2,b2,w3,b3]
    return x_generate,g_params


def build_discriminator(x_data,x_generated,keep_prob):
    #将real img 和 generated img拼在一起
    x_in = tf.concat([x_data,x_generated],0)
    w1 = tf.Variable(tf.truncated_normal([img_size,h2_size],stddev=0.1),name='d_w1',dtype=tf.float32)
    b1 = tf.Variable(tf.zeros([h2_size]),name='d_b1',dtype=tf.float32)
    h1 = tf.nn.dropout(tf.nn.relu(tf.matmul(x_in,w1)+b1),keep_prob)
    w2 = tf.Variable(tf.truncated_normal([h2_size,h1_size],stddev=0.1),name='d_w2',dtype=tf.float32)
    b2 = tf.Variable(tf.zeros([h1_size]),name='d_b2',dtype=tf.float32)
    h2 = tf.nn.dropout(tf.nn.relu(tf.matmul(h1,w2)+b2),keep_prob)
    w3 = tf.Variable(tf.truncated_normal([h1_size,1]),name='d_w3',dtype=tf.float32)
    b3 = tf.Variable(tf.zeros([1]),name='d_b3',dtype=tf.float32)
    h3 = tf.matmul(h2,w3)+b3
    
    """
    h3的size:[batch_size + batch_size,1]
    所以 y_data 是对 real img的判别结果
    y_generated 是对 generated img 的判别结果
    """
    y_data = tf.nn.sigmoid(tf.slice(h3,[0,0],[batch_size,-1],name=None))
    y_generated = tf.nn.sigmoid(tf.slice(h3,[batch_size,0],[-1,-1],name=None))
    d_params = [w1,b1,w2,b2,w3,b3]
    return y_data,y_generated,d_params


