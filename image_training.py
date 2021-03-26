#-*- coding:utf-8 -*

import numpy as np
import image_process, image_feature, image_model

def main():
    # image_process.main() #处理原始验证码，并存到文件
    # feature, label = image_feature.main() #特征处理

    #特征处理
    image_array, label = image_feature.read_train_data()
    feature = []
    for num, image in enumerate(image_array):
        feature_vec = image_feature.feature_transfer(image)
        # print('label: ',image_label[num])
        # print(feature)
        feature.append(feature_vec)
    print(np.array(feature).shape)
    print(np.array(label).shape)

    #训练模型
    result = image_model.trainModel(feature, label)

if __name__ == '__main__': main()
