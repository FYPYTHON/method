# coding=utf-8
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
x_init = tf.constant([[0.7,0.9]])    # batch
w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
w2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
# 定义placeholder作为存储输入数据的地方，维度定义好可以降低出错的概率
x = tf.placeholder(tf.float32,shape=(1,2), name="input")
# x = tf.placeholder(tf.float32,shape=(3,2), name="input")
y_ = tf.placeholder(tf.float32,shape=(None,1), name="y_input")
a = tf.matmul(x, w1)
y = tf.matmul(a, w2)

sess = tf.Session()
init_op = tf.global_variables_initializer()
sess.run(init_op)
print(sess.run(y, feed_dict={x:[[0.7,0.9]]}))
# print(sess.run(y, feed_dict={x:[[0.7,0.9],[0.1,0.4],[0.5,0.8]]}))

y = tf.sigmoid(y)  # 将值映射为 [0,1] y表示正样本的概率 1-y表示负
# 定义损失函数刻画 预测值与真实值的差距
# 交叉熵 cross_entropy

print("1-y:",tf.log(tf.clip_by_value(1-y, 1e-10, 1.0)))
cross_entropy = - tf.reduce_mean(
    y * tf.log(tf.clip_by_value(y, 1e-10, 1.0))
    + (1-y_) * tf.log(tf.clip_by_value(1-y, 1e-10, 1.0))
    )

# 定义学习效率
learning_rate = 0.001

# 定义反向传播算法优化神经网络中的参数
# 优化方法 tf.train.GradientDescentOptimizer tf.train.MomentumOptimizer等

train_step = \
    tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)