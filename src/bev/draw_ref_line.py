#-*-coding:UTF-8-*-
'''
Created on 2017��8��10��-����5:25:51
author: Gary-W
# ��BEV�У����ƺ����Լ�����Ĳο���
'''
import cv2
import numpy as np
from dataio import get_filelist

# root = r"E:\LOC_Code_Dataset\saic_dataset\oflim�������\ofilm_raw_data_ug\20170807_EP21_car02\01_��ڽ�����ֱ��������ҳ�������Ȧ���\bev\7x7_(-1--1)"
# imlist = get_filelist(root, ".jpg")
# for path in imlist:
#     img = cv2.imread(path)
#     h,w,_ = img.shape
#     center = w/2
#     cv2.line(img, (center,0),(center,h-1),(200,100,200),1)
#     c = 225
#     cv2.line(img, (0,c),(h-1,c),(200,100,200),1)
#     cv2.imwrite(path, img)
#     # cv2.imshow("img", img)
#     # cv2.waitKey(0)

"""
road width: 96 pix 4.05 m
lot width: 46 pix 2.35 m

print 96.0 / 4.05, 47.0 / 2.35
print (236-103) / 5.58, (184-139) / 2.35
"""

print 98.0 / 3.01, 54.0 / 1.97
print (236-103) / 5.58, (184-139) / 2.35

if __name__=="__main__":
    pass

