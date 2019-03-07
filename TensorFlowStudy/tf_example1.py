# coding=utf-8
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
from numpy.random import RandomState
# 定义训练数据batch的大小
batch_size = 8
# 定义神经网路参数
w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
# 在shape的一个维度上使用none 可以方便使用不同的batch大小
x = tf.placeholder(tf.float32, shape=(None, 2), name="x_input")
y_ = tf.placeholder(tf.float32, shape=(None, 1), name="y_input")
# 定义神经网络前向传播的过程
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

# 定义损失函数 和 反向传播的算法
y = tf.sigmoid(y)
cross_entropy = -tf.reduce_mean(
    y_ * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
    + (1-y_) * tf.log(tf.clip_by_value(1-y, 1e-10, 1.0))
    )
train_step = \
    tf.train.AdamOptimizer(0.001).minimize(cross_entropy)

# 通过随机数生成一个模拟数据集
rdm = RandomState(1)
dataset_size = 128
X = rdm.rand(dataset_size, 2)
print("X:",X)

# 定义规则 x1+x2 < 1 为正 其他为负
# 0 = 负  1 = 正
Y = [[int(x1 + x2 < 1)] for (x1,x2) in X]
print("Y:",Y)

# 创建会话运行TensorFlow程序
with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    print("w1:",sess.run(w1))
    print("w2:",sess.run(w2))
    # 设置训练轮数
    STEPS = 5000
    for i in range(5000):
        # 每次选取batch_size个样本进行训练
        start = (i * batch_size) % dataset_size
        end = min(start + batch_size,dataset_size)
        # 通过选取的样本训练神经网络兵更新参数
        sess.run(train_step, feed_dict={x:X[start:end],y_:Y[start:end]})
        if i % 1000 == 0:
            # 每隔一段时间计算在所有数据上的交叉熵并输出
            total_cross_entropy = sess.run(
                cross_entropy, feed_dict={x:X, y_:Y})
            print("After %d training steps,cross entropy on all data is %g"%(i,total_cross_entropy))
    print("After train w1:\n",sess.run(w1))
    print("After train w2:\n",sess.run(w2))