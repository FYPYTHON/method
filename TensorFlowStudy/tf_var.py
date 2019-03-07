# coding=utf-8
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print ("this is a test code.")
import tensorflow as tf
weights = tf.Variable(tf.random_normal([2,3],stddev=2))
# print(weights)
x = tf.constant([[0.7,0.9]])
w1 = tf.Variable(tf.random_normal((2,3),stddev=1),name="w1")
w2 = tf.Variable(tf.random_normal([2,3],stddev=1,dtype=tf.float64),name="w2")
# tf.assign(w1,w2)   # 初始化变量
w3 = tf.Variable(tf.random_normal((2,2),stddev=1),name="w3")
# tf.assign(w1,w3,validate_shape=False)   # 初始化变量,维度改变

# print(tf.global_variables)  # 获取所有变量
# print(tf.trainable_variables)
# print(w1,w2,w3)
a = tf.matmul(x,w1)
sess = tf.Session()
sess.run(w1.initializer)
print(sess.run(w1))
print(sess.run(a))
sess.run(w2.initializer)
print(sess.run(w2))
sess.close()