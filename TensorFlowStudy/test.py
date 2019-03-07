# coding=utf-8
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
print ("this is a test code.")
# http://playground.tensorflow.org/
# python3 -m pip install --upgrade pip
import tensorflow as tf
a = tf.constant([1.0,2.0],name='a')
b = tf.constant([3.0,4.0],name='b')
result = a + b
sess = tf.Session()
sess.run(result)

print(sess.run(result))   # 查看取值
print(result.eval(session=sess)) # 查看取值
# sess2 = tf.InteractiveSession()  # 交互式
# print(result.eval())
print(a.graph is result.graph)
print(result)
sess.close()
