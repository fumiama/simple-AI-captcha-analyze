#-*- coding:utf-8 -*

from PIL import Image
import random
import os
import time
import random
import image_training
from config import *
import numpy as np

def read_captcha(path):
    """
    读取验证码图片
    :param path: 原始验证码存放路径
    :return: image_array, image_label：存放读取的iamge list和label list
    """
    image_label = []
    image_clean = []
    file_list = os.listdir(path)#获取captcha文件
    for i, f in enumerate(file_list):
        fp = open(path + '/' + f, "rb")
        image = Image.open(fp)#打开图片
        file_name = f.split(".")[0]
        image_clean.append(image_transfer(i ,image))
        fp.close()
        image_label.append(file_name)
    return image_label, image_clean

def image_transfer(i, image, captcha_clean_save = False):
    """
    图像粗清理
    将图像转换为灰度图像，将像素值小于某个值的点改成白色
    :param image_arry:
    :param captcha_clean_save:
    :return: image_clean:清理过后的图像list
    """
    image = image.convert('L') #转换为灰度图像，即RGB通道从3变为1
    im2 = Image.new("L", image.size, 255)

    for y in range(image.size[1]): #遍历所有像素，将灰度超过阈值的像素转变为255（白）
        for x in range(image.size[0]):
            pix = image.getpixel((x, y))
            if int(pix) > threshold_grey:  #灰度阈值
                im2.putpixel((x, y), 255)
            else:
                im2.putpixel((x, y), pix)

    if captcha_clean_save: #保存清理过后的iamge到文件
        im2.save(captcha_clean_path + '/' + image_label[i] + '.jpg')
    return im2

def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
    :param img: Image
    :param x:
    :param y:
    :return:
    """
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum

def remove_noise_pixel(img, noise_point_list):
    """
    根据噪点的位置信息，消除二值图片的黑点噪声
    :type img:Image
    :param img:
    :param noise_point_list:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)

def get_clear_bin_image(image):
    """
    图像细清理
    获取干净的二值化的图片。
    图像的预处理：
    1. 先转化为灰度
    2. 再二值化
    3. 然后清除噪点
    参考:http://python.jobbole.com/84625/
    :type img:Image
    :return:
    """

    table = get_bin_table()
    out = image.point(table, '1')  # 变成二值图片:0表示黑色,1表示白色

    noise_point_list = []  # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
    for x in range(out.width):
        for y in range(out.height):
            res_9 = sum_9_region(out, x, y)
            if (0 < res_9 < 4) and out.getpixel((x, y)) == 0:  # 找到孤立点
                pos = (x, y)  #
                noise_point_list.append(pos)
    remove_noise_pixel(out, noise_point_list)
    return out

def image_split(image):
    """
    图像切割
    :param image:单幅图像
    :return:单幅图像被切割后的图像list
    """
    #切割图片
    image_split_array = []
    w = image.width // 4
    for i in range(image_character_num):
        # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
        im_split = image.crop((w * i, 0, w * (i + 1), image.height))
        im_split = im_split.resize((image_width, image_height))
        image_split_array.append(im_split)
    return image_split_array

def image_save(image_array, image_label):
    """
    保存图像到文件
    :param image_array: 切割后的图像list
    :param image_label: 图像的标签
    :return:
    """
    for num, image_meta in enumerate(image_array):
        file_path = train_data_path + "/" + image_label[num] + '/'
        file_name = str(int(time.time())) + '_' + str(random.randint(0,100)) + '.gif'
        if not os.path.exists(file_path): os.makedirs(file_path)
        image_meta.save(file_path  + file_name, 'gif')

def main():
    image_label, image_clean = read_captcha(train_data_tmp_path) #读取验证码文件

    for k, each_image in enumerate(image_clean):
        image_out = get_clear_bin_image(each_image) #验证码图像细清理
        split_result = image_split(image_out) #图像切割
        image_save(split_result, image_label[k]) #保存训练图像

if __name__ == '__main__': main()
