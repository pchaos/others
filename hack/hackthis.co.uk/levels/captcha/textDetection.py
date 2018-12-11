# coding:utf8

'''
文字区域的提取
原文地址： https://blog.csdn.net/huobanjishijian/article/details/63685503
'''

import numpy as np
import sys, os
import glob
import random

import cv2

def getRandomImg(imgFolder=None):
    '''

    :return: 随机返回图片文件名
    '''
    # 默认图片目录
    if not imgFolder:
        CAPTCHA_IMAGE_FOLDER = "captcha"
    # Get a list of all the captcha images we need to process
    captcha_image_files = glob.glob(os.path.join(CAPTCHA_IMAGE_FOLDER, "*.png"))
    return captcha_image_files[int(random.random()*len(captcha_image_files))]

def preprocess(gray, ksize1=(30, 9), ksize2=(24, 6)):
    # 1. Sobel算子，x方向求梯度
    sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
    # 2. 二值化
    ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    # 3. 膨胀和腐蚀操作的核函数
    element1 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize1)
    element2 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize2)

    # 4. 膨胀一次，让轮廓突出
    dilation = cv2.dilate(binary, element2, iterations=1)

    # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
    erosion = cv2.erode(dilation, element1, iterations=1)

    # 6. 再次膨胀，让轮廓明显一些
    dilation2 = cv2.dilate(erosion, element2, iterations=3)

    # 7. 存储中间图片
    tmpPath = '/tmp'  #临时目录
    cv2.imwrite(os.path.join(tmpPath, "binary.png"), binary)
    cv2.imwrite(os.path.join(tmpPath, "dilation.png"), dilation)
    cv2.imwrite(os.path.join(tmpPath, "erosion.png"), erosion)
    cv2.imwrite(os.path.join(tmpPath, "dilation2.png"), dilation2)

    return dilation2


def findTextRegion(img):
    region = []

    # 1. 查找轮廓
    im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 2. 筛选那些面积小的
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算该轮廓的面积
        area = cv2.contourArea(cnt)

        # 面积小的都筛选掉
        if (area < 1000):
            continue

        # 轮廓近似，作用很小
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 找到最小的矩形，该矩形可能有方向
        rect = cv2.minAreaRect(cnt)
        print("rect is: ")
        print(rect)

        # box是四个点的坐标
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])

        # 筛选那些太细的矩形，留下扁的
        if (height > width * 1.2):
            continue

        region.append(box)

    return region


def detect(sourceImg, targetImage='/tmp/contours.png'):
    # 1.  转化成灰度图
    gray = cv2.cvtColor(sourceImg, cv2.COLOR_BGR2GRAY)

    # 2. 形态学变换的预处理，得到可以查找矩形的图片
    dilation = preprocess(gray, (5, 3), (5,3))

    # 3. 查找和筛选文字区域
    region = findTextRegion(dilation)

    # 4. 用绿线画出这些找到的轮廓
    for box in region:
        cv2.drawContours(sourceImg, [box], 0, (0, 255, 0), 2)

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img", sourceImg)

    # 带轮廓的图片
    cv2.imwrite(targetImage, sourceImg)

    cv2.waitKey(1800)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 读取文件
    try:
        # imagePath = sys.argv[1]
        imagePath = 'textDetection.png'
    except Exception as e:
        imagePath = getRandomImg()
    img = cv2.imread(imagePath)
    detect(img)

    for i in range(10):
        try:
            imagePath = sys.argv[1]
            # imagePath = 'textDetection.png'
        except Exception as e:
            imagePath = getRandomImg()
            print('image name: {}'.format(imagePath))
        img = cv2.imread(imagePath)
        detect(img)

