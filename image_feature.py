#-*- coding:utf-8 -*


import os
from PIL import Image
import image_training
import configparser
import config as c

def read_train_data():
    """
    读取训练集文件夹下的单字母/数字图像文件
    :return:image_array, image_label:图像list、图像label list
    """
    image_array = []
    image_label = []
    image_feature = []
    for label in os.listdir(c.train_data_path):#获取目录下的所有文件
        label_path = c.train_data_path + '/' + label
        for image_path in os.listdir(label_path):
            fp = open(label_path + '/' + image_path, "rb")
            image = Image.open(fp)
            image_array.append(image)
            image_label.append(label)
            image_feature.append(feature_transfer(image))
            fp.close()
    return image_array, image_label

#feature generated
def feature_transfer(image):
    """
    生成特征矩阵
    计算每副图像的行和、列和，共c.image_width + c.image_height个特征
    :param image:图像list
    :return:
    """
    image = image.resize((c.image_width, c.image_height)) #标准化图像格式

    feature = []#计算特征
    for x in range(c.image_width):#计算行特征
        feature_width = 0
        for y in range(c.image_height):
            if image.getpixel((x, y)) == 0:
                feature_width += 1
        feature.append(feature_width)

    for y in range(c.image_height): #计算列特征
        feature_height = 0
        for x in range(c.image_width):
            if image.getpixel((x, y)) == 0:
                feature_height += 1
        feature.append(feature_height)
    # print('feature length :',len(feature))
    return feature

def main():
    return read_train_data()

if __name__ == '__main__': main()
