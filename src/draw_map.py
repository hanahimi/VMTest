#-*-coding:UTF-8-*-
'''
Created on 2017年1月12日-下午3:30:08
author: Gary-W

地图绘制，坐标点投影
'''
import cv2
import numpy as np

class CarModel:
    def __init__(self, car_file):
        self.img = cv2.imread(car_file)
        self.img = cv2.resize(self.img, (32,32))
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        
    def get_rot(self, yaw_deg):
        M = cv2.getRotationMatrix2D((self.cols/2,self.rows/2), - yaw_deg,1)
        dst = cv2.warpAffine(self.img,M,(self.cols,self.rows))
        return dst

class PosMap:
    """ 地图绘制类
    用于将世界坐标映射到图片上，可以使用配置文件进行参数设置
    attribute:
      map_img: 原始地图数据
      coef: 坐标投影参数
    """
    def __init__(self,config_table):
        self.map_path = config_table["map_path"]
        self.map_img = cv2.imread(self.map_path)
        self.coef = config_table["project_factors"]
        self.w_offset = config_table["world_center_offset"]
        self.ischanged = False
        car_file = config_table["car_path"]
        self.car_logo = CarModel(car_file)
    
    def compare_position(self, gtx, gty, gtyaw, dtx,dty,dtyaw):
        """ 对比GT点的位置(红色) 和 预测点的位置(绿色)
        output:
          map_img: 系统图像的当前状态
        """
        gtx += self.w_offset[0]
        gty += self.w_offset[1]
        
        dtx += self.w_offset[0]
        dty += self.w_offset[1]

        pil_x_gt = int(1.0 * gtx * self.coef[2] + self.coef[0])
        pil_y_gt = int(1.0 * gty * self.coef[3] + self.coef[1])
        cv2.circle(self.map_img,(pil_x_gt,pil_y_gt),2,(117,152,253),-1)
        
        pil_x_dt = int(1.0 * dtx * self.coef[2] + self.coef[0])
        pil_y_dt = int(1.0 * dty * self.coef[3] + self.coef[1])
        cv2.circle(self.map_img,(pil_x_dt,pil_y_dt),2,(244,254,129),-1)
        
        cv2.line(self.map_img,(pil_x_gt,pil_y_gt),(pil_x_dt,pil_y_dt),(233,132,251),1)
        
        return self.map_img
    
    def mark_position(self, pos_x, pos_y, pos_yaw):
        """ 将世界坐标系的点记录到图像中，改写原有图像
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: 系统图像的当前状态
        """
        pos_x += self.w_offset[0]
        pos_y += self.w_offset[1]

        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        
        cv2.circle(self.map_img,(pil_x,pil_y),1,(19,162,247),-1)
        self.ischanged = True

        return self.map_img
    
    def mark_position_id(self, pos_x, pos_y, pos_yaw, _id, step=100):
        """ 将世界坐标系的点记录到图像中，改写原有图像
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: 系统图像的当前状态
        """
        pos_x += self.w_offset[0]
        pos_y += self.w_offset[1]
        
        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        
        cv2.circle(self.map_img,(pil_x,pil_y),1,(19,162,247),-1)
        if _id % step==0:
            cv2.putText(self.map_img, str(_id),(pil_x,pil_y),  
                        cv2.FONT_HERSHEY_PLAIN, 1, (19,24,24), thickness = 1,)
            cv2.circle(self.map_img,(pil_x,pil_y),3,(19,24,24),-1)
        self.ischanged = True

        return self.map_img
        
    def project_position(self, pos_x, pos_y, pos_yaw):
        """ 将世界坐标系的点记录到图像中，将改写原有图像
            当原有的图像发生过改变时，读入新的图像
        input:
          pos_x, pos_y, pos_yaw(deg)
        output:
          proj_img: 结果图像
        """
        if self.ischanged:
            proj_img = cv2.imread(self.map_path)
        else:
            proj_img = np.copy(self.map_img)

        car_img = self.car_logo.get_rot(pos_yaw)
        h,w,_ = car_img.shape
        
        pos_x += self.w_offset[0]
        pos_y += self.w_offset[1]

        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        sub_roi = proj_img[pil_y-h/2:pil_y+h/2, pil_x-w/2:pil_x+w/2,:]
        
        sub_roi[car_img!=0] = car_img[car_img!=0]
        return proj_img

    def disp_map(self):
        cv2.imshow("map",self.map_img)
        cv2.waitKey(0)

 
if __name__=="__main__":
    pass

