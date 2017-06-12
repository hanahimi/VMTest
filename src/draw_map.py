#-*-coding:UTF-8-*-
'''
Created on 2017��1��12��-����3:30:08
author: Gary-W

��ͼ���ƣ������ͶӰ
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
    """ ��ͼ������
    ���ڽ���������ӳ�䵽ͼƬ�ϣ�����ʹ�������ļ����в�������
    attribute:
      map_img: ԭʼ��ͼ����
      coef: ����ͶӰ����
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
        """ �Ա�GT���λ��(��ɫ) �� Ԥ����λ��(��ɫ)
        output:
          map_img: ϵͳͼ��ĵ�ǰ״̬
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
        """ ����������ϵ�ĵ��¼��ͼ���У���дԭ��ͼ��
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: ϵͳͼ��ĵ�ǰ״̬
        """
        pos_x += self.w_offset[0]
        pos_y += self.w_offset[1]

        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        
        cv2.circle(self.map_img,(pil_x,pil_y),1,(19,162,247),-1)
        self.ischanged = True

        return self.map_img
    
    def mark_position_id(self, pos_x, pos_y, pos_yaw, _id, step=100):
        """ ����������ϵ�ĵ��¼��ͼ���У���дԭ��ͼ��
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: ϵͳͼ��ĵ�ǰ״̬
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
        """ ����������ϵ�ĵ��¼��ͼ���У�����дԭ��ͼ��
            ��ԭ�е�ͼ�������ı�ʱ�������µ�ͼ��
        input:
          pos_x, pos_y, pos_yaw(deg)
        output:
          proj_img: ���ͼ��
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

