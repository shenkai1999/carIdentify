#沈楷
import os
import numpy as np
from PIL import Image
from skimage import io,transform
import random
import tensorflow as tf
import matplotlib.pyplot as plt
from numpy import *

bus=[]
bus_label=[]
truck=[]
truck_label=[]
motor=[]
motor_label=[]
car=[]
car_label=[]
tricycle=[]
tricycle_label=[]
van = []
van_label = []
ratio = 0.2 #测试集占总样本量的比例
def get_file(fir_dir):
    for file in os.listdir(fir_dir+"/bus"):
        bus.append(fir_dir+"/bus"+"/"+file)
        bus_label.append(0)
    for file in os.listdir(fir_dir+"/truck"):
        truck.append(fir_dir+"/truck"+"/"+file)
        truck_label.append(1)
    for file in os.listdir(fir_dir+"/motor"):
        motor.append(fir_dir+"/motor"+"/"+file)
        motor_label.append(2)
    for file in os.listdir(fir_dir+"/littlecar"):
        car.append(fir_dir+"/littlecar"+"/"+file)
        car_label.append(3)
    for file in os.listdir(fir_dir+"/tricycle"):
        tricycle.append(fir_dir+"/tricycle"+"/"+file)
        tricycle_label.append(4)
    for file in os.listdir(fir_dir + "/van"):
        van.append(fir_dir + "/van" + "/" + file)
        van_label.append(5)

    print("There are %d bus\nThere are %d truck\nThere are %d motor\nThere are %d car\nThere are %d tricycle\nThere are %d van\n" %(len(bus), len(truck),len(motor),len(car),len(tricycle),len(van)),end="")
    image_list = np.hstack((bus,truck,motor,car,tricycle,van))
    label_list = np.hstack((bus_label,truck_label,motor_label,car_label,tricycle_label,van_label))

    temp = np.array([image_list,label_list])
    temp = temp.transpose()
    np.random.shuffle(temp)#打乱顺序
    all_image_list = list(temp[:,0])  # 取出第0列数据，即图片路径
    all_label_list = list(temp[:,1])    # 取出第1列数据，即图片标签
    label_list = [int(i) for i in label_list]   # 转换成int数据类型

    n_sample = len(all_label_list)
    n_val = int(math.ceil(n_sample*ratio)) #验证集样本数
    n_train = n_sample-n_val  #训练样本数
    tra_images = all_image_list[0:n_train]
    tra_labels = all_label_list[0:n_train]
    tra_labels = [int(float(i)) for i in tra_labels]
    val_images = all_image_list[n_train:-1]
    val_labels = all_label_list[n_train:-1]
    val_labels = [int(float(i)) for i in val_labels]
    return tra_images,tra_labels,val_images,val_labels




# 将image和label转为list格式数据，因为后边用到的的一些tensorflow函数接收的是list格式数据

# 为了方便网络的训练，输入数据进行batch处理

# image_W, image_H, ：图像高度和宽度

# batch_size：每个batch要放多少张图片

# capacity：一个队列最大多少

def get_batch(image, label, image_W, image_H, batch_size, capacity):
    # step1：将上面生成的List传入get_batch() ，转换类型，产生一个输入队列queue

    # tf.cast()用来做类型转换

    image = tf.cast(image, tf.string)  # 可变长度的字节数组.每一个张量元素都是一个字节数组

    label = tf.cast(label, tf.int32)

    # tf.train.slice_input_producer是一个tensor生成器

    # 作用是按照设定，每次从一个tensor列表中按顺序或者随机抽取出一个tensor放入文件名队列。

    input_queue = tf.train.slice_input_producer([image, label])

    label = input_queue[1]

    image_contents = tf.io.read_file(input_queue[0])  # tf.read_file()从队列中读取图像

    # step2：将图像解码，使用相同类型的图像

    image = tf.image.decode_jpeg(image_contents, channels=3)

    # jpeg或者jpg格式都用decode_jpeg函数，其他格式可以去查看官方文档

    # step3：数据预处理，对图像进行旋转、缩放、裁剪、归一化等操作，让计算出的模型更健壮。

    image = tf.image.resize_images (image, [image_W,image_H],method=0)

    # 对resize后的图片进行标准化处理

    image = tf.image.per_image_standardization(image)

    # step4：生成batch

    # image_batch: 4D tensor [batch_size, width, height, 3], dtype = tf.float32

    # label_batch: 1D tensor [batch_size], dtype = tf.int32

    image_batch, label_batch = tf.train.batch([image, label], batch_size=batch_size, num_threads=16, capacity=capacity)

    # 重新排列label，行数为[batch_size]

    label_batch = tf.reshape(label_batch, [batch_size])

    #image_batch = tf.cast(image_batch, tf.uint8)    # 显示彩色图像

    image_batch = tf.cast(image_batch, tf.float32)  # 显示灰度图

    # print(label_batch) Tensor("Reshape:0", shape=(6,), dtype=int32)



    return image_batch, label_batch

    # 获取两个batch，两个batch即为传入神经网络的数据





# image_list, label_list, val_images, val_labels = get_file(train_dir)

