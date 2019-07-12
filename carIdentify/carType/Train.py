'''
沈楷
Train.py

对搭建好的网络进行训练，并保存训练参数，以便下次使用



'''

# 导入文件

import os

import numpy as np

import tensorflow as tf

from webServer.Prework import get_file, get_batch

from webServer.CNNmodel import deep_CNN, losses, trainning, evaluation

# 变量声明

N_CLASSES = 6

IMG_W = 28  # resize图像，太大的话训练时间久

IMG_H = 28

BATCH_SIZE = 20  # 每个batch要放多少张图片

CAPACITY = 200  # 一个队列最大多少

MAX_STEP = 1200

learning_rate = 0.0001  # 一般小于0.0001

# 获取批次batch

train_dir = 'G:/car'  # 训练样本的读入路径

logs_train_dir = './CK+_part'  # logs存储路径

train, train_label,val,val_lable = get_file(train_dir)

# 训练数据及标签

train_batch, train_label_batch = get_batch(train, train_label, IMG_W, IMG_H, BATCH_SIZE, CAPACITY)
val_batch,val_label_batch = get_batch(val,val_lable,IMG_W,IMG_H,BATCH_SIZE,CAPACITY)

# 训练操作定义

train_logits = deep_CNN(train_batch, BATCH_SIZE, N_CLASSES)

train_loss = losses(train_logits, train_label_batch)

train_op = trainning(train_loss, learning_rate)#损失值优化

train_acc = evaluation(train_logits, train_label_batch)

#测试操作定义

test_logits = deep_CNN(val_batch, BATCH_SIZE, N_CLASSES)
test_loss = losses(test_logits, val_label_batch)

test_acc = evaluation(test_logits, val_label_batch)

# 这个是log汇总记录

summary_op = tf.compat.v1.summary.merge_all()

# 产生一个会话

sess = tf.compat.v1.Session()

train_writer = tf.compat.v1.summary.FileWriter(logs_train_dir, sess.graph)

# 产生一个saver来存储训练好的模型

saver = tf.compat.v1.train.Saver(max_to_keep=1)

# 所有节点初始化

sess.run(tf.compat.v1.global_variables_initializer())

# 队列监控

coord = tf.train.Coordinator()  # 设置多线程协调器

threads = tf.train.start_queue_runners(sess=sess, coord=coord)

# 进行batch的训练

try:

    # 执行MAX_STEP步的训练，一步一个batch

    for step in np.arange(MAX_STEP):

        if coord.should_stop():
            break

        # 启动以下操作节点，有个疑问，为什么train_logits在这里没有开启？

        _, tra_loss, tra_acc = sess.run([train_op, train_loss, train_acc])

        # 每隔100步打印一次当前的loss以及acc，同时记录log，写入writer

        if step % 100 == 0:
            print('Step %d, train loss = %.2f, train accuracy = %.2f%%' % (step, tra_loss, tra_acc * 100.0))

            summary_str = sess.run(summary_op)

            train_writer.add_summary(summary_str, step)

        checkpoint_path = os.path.join(logs_train_dir, 'thing.ckpt')

        saver.save(sess, checkpoint_path)  # 每隔100步，保存一次训练好的模型

        if (step + 1) == MAX_STEP:

            checkpoint_path = os.path.join(logs_train_dir, 'thing.ckpt')

            saver.save(sess, checkpoint_path, global_step=step)  # 保存最后一次网络参数


except tf.errors.OutOfRangeError:

    print('Done training -- epoch limit reached')

finally:

    coord.request_stop()

coord.join(threads)

sess.close()