'''
沈楷
Test.py


'''



import os

import numpy as np

from PIL import Image

import tensorflow as tf

import matplotlib.pyplot as plt

from webServer.CNNmodel import deep_CNN

N_CLASSES = 6

img_dir = 'G:/car/test/'

log_dir = './CK+_part/'

lists = ['巴士', '卡车','摩托','小汽车','三轮车',"面包车"]


# 从测试集中随机挑选一张图片看测试结果

def get_one_image(img_dir):
        imgs = os.listdir(img_dir)
        img_num = len(imgs)
        idn = np.random.randint(0, img_num)
        image = imgs[idn]
        image_dir = img_dir + image
        print(image_dir)
        image = Image.open(image_dir)
        plt.imshow(image)
        plt.show()
        image = image.resize((28,28))
        image_arr = np.array(image)
        return image_arr

def Mytest(IMAGE_ARR):
        with tf.Graph().as_default():
            image = tf.cast(IMAGE_ARR, tf.float32)

            image = tf.image.per_image_standardization(image)

            image = tf.reshape(image, [1, 28, 28, 3])

            # print(image.shape)

            p = deep_CNN(image, 1, N_CLASSES) #将需要识别的图片放进神经网络

            logits = tf.nn.softmax(p) #归一化

            x = tf.placeholder(tf.float32, shape=[28, 28, 3])

            saver = tf.train.Saver()

            sess = tf.Session()

            sess.run(tf.global_variables_initializer()) #variable初始化

            ckpt = tf.train.get_checkpoint_state(log_dir)

            if ckpt and ckpt.model_checkpoint_path:
                # print(ckpt.model_checkpoint_path)

                saver.restore(sess, ckpt.model_checkpoint_path)

                # 调用saver.restore()函数，加载训练好的网络模型

                print('Loading success')

            prediction = sess.run(logits, feed_dict={x: IMAGE_ARR})

            max_index = np.argmax(prediction)

            print('预测的标签为：', max_index, lists[max_index])

            print('预测的结果为：', prediction)
            return lists[max_index]
if __name__ == '__main__':

    image_arr = get_one_image(img_dir)
    Mytest(image_arr)
    '''
    img_dir = 'E:/IdentifyType/webServer/static/image/test.jpg'
    image = Image.open(img_dir)
    image = image.resize((28, 28))
    image_arr = np.array(image)
    Mytest(image_arr)
    '''