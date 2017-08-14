#-*-coding:UTF-8-*-
'''
Created on 2017年7月27日-下午6:58:41
author: Gary-W
'''

import cv2
from numpy import sqrt
import numpy as np

class Point2f:
    def __init__(self,x=None, y=None):
        self.x = x
        self.y = y
    def __str__(self):
        return "x:%3.2f, y:%3.2f" % (self.x, self.y)

def calc_orc_result(carPoint0, carPoint3, worldPoint0, worldPoint3):
    # 车辆坐标系下 库位的位置 carPoint0,carPoint1
    # 世界坐标系下 库位的位置 worldPoint0, worldPoint1
    # return 车辆的位置
    vector_car = Point2f(0,0)
    vector_car.x = carPoint3.x - carPoint0.x;
    vector_car.y = carPoint3.y - carPoint0.y;
    
    vector_wrold = Point2f(0,0)
    vector_wrold.x = worldPoint3.x - worldPoint0.x
    vector_wrold.y = worldPoint3.y - worldPoint0.y

    print vector_car
    print vector_wrold
    
    modcar_world = sqrt(vector_wrold.y*vector_wrold.y + vector_wrold.x*vector_wrold.x)*sqrt(vector_car.y*vector_car.y + vector_car.x*vector_car.x)
    
#     //sin_theta = (vector_wrold.x*vector_car.y - vector_wrold.y*vector_car.x) / modcar_world
#     //cos_theta = (vector_wrold.x*vector_car.x + vector_wrold.y*vector_car.y) / modcar_world
#     
    sin_theta = (vector_car.x*vector_wrold.y - vector_car.y*vector_wrold.x) / modcar_world
    cos_theta = (vector_car.x*vector_wrold.x + vector_car.y*vector_wrold.y) / modcar_world
    print "sin:",sin_theta, "cos:",cos_theta
    print "deg:", np.rad2deg(np.arccos(cos_theta) * (1 if (sin_theta>0) else -1))
    
    print
    print "worldPoint0:",worldPoint0
    print "worldPoint3:",worldPoint3
    print "carPoint0:",carPoint0
    print "carPoint3:",carPoint3
    print
    a = worldPoint0.x - carPoint0.x*cos_theta + carPoint0.y*sin_theta
    b = worldPoint0.y - carPoint0.x*sin_theta - carPoint0.y*cos_theta

    ocrresult = Point2f(0,0) 
    ocrresult.x = a
    ocrresult.y = b
    
    return ocrresult

def load_data():
    # car0.x, car0.y car3.x, car3.y, w0.x, w0.y w3.x, w3.y 

    data = [151,508,-74,508, 
            301,902,301,437]
#     data = [224.61,-265.48,5.05,-329.95,    # diaotou
#             2517,2311,2517,2082]
    
    carPoint0 = Point2f(data[0],data[1])
    carPoint3 = Point2f(data[2],data[3])
    worldPoint0 =Point2f(data[4],data[5])
    worldPoint3 =Point2f(data[6],data[7])

    ocrresult = calc_orc_result(carPoint0, carPoint3, worldPoint0, worldPoint3)
    print ocrresult
    
def main():
    load_data()
    
if __name__=="__main__":
    pass
    main()






