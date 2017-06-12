#-*-coding:UTF-8-*-
'''
Created on 2016��12��17��
@author: DL

�˶�ģ����أ����ڽ���can�źŲ�ת��Ϊλ������
'''
import numpy as np

FLT_MIN = 1.175494351e-38

_Forward_R = 0
_Forward_L = 1
_Backward_R = 2
_Backward_L = 3

TIME_SCALE = 1

class CanMatchLog:
    """ ��һ��can_match���ݽ��з�װ
    """
    def __init__(self, can_log=None):
        self.data = {}
        if can_log!=None:
            self.setCan(can_log)
        
    def setCan(self, str_can_log):
        """ ��ȡcan_log(str),����can��Ϣ
            ÿ�� can_log ���� can_data.txt �����һ����Ϣ
        """
        items = str_can_log.strip("\n").split(" ")
        strframeId, str_can_data = items[0], items[1:]
        self.data["frameID"] = int(strframeId)
        can_data = [float(item) for item in str_can_data]

        speed_unit = 3.6
        
        self.data["time_stamp"] = int(can_data[0])   # us
        self.data["shift_pos"] = can_data[1]
        self.data["steering_angle"] = can_data[2]   # deg
        self.data["vehicle_speed"] = can_data[3]/speed_unit    # kmh
        self.data["yaw_rate"] = can_data[4]         # deg/s
        self.data["wheel_speed_rl"] = can_data[5]/speed_unit   # kmh
        self.data["wheel_speed_fl"] = can_data[6]/speed_unit   # kmh
        self.data["wheel_speed_rr"] = can_data[7]/speed_unit   # kmh
        self.data["wheel_speed_fr"] = can_data[8]/speed_unit   # kmh
    
    def __repr__(self):
        return "%d %d %d %f %f" % (self.data["frameID"], self.data["time_stamp"], self.data["shift_pos"],
                                   self.data["steering_angle"], self.data["vehicle_speed"])

def can_insert(can_log_a, can_log_b, times):
    """ �� can_log_a �� can_log_b ֮����� times ���ؼ�֡
    ���� can_log �б��б��0��Ԫ��Ϊ can_log_a,���һ��Ԫ��Ϊ can_log_b
    """
    can_log_inserted = []
    for i in range(times):
        _can_log = CanMatchLog()
        for key in can_log_a.data.keys():
            vd = can_log_b.data[key] - can_log_a.data[key]
            vd = vd * i / times
            _can_log.data[key] = can_log_a.data[key] + vd
        can_log_inserted.append(_can_log)
    
    can_log_inserted.append(can_log_b)

    return can_log_inserted
        

        
class VehicleMotion:
    """ �����˶�ģ��
    ͨ������can��Ϣ���㳵�����˶�״̬
    �� GongHow ��cpp����ֱ��ת���õ�
    """
    class Point:
        def __init__(self):
            self.x = 0
            self.y = 0
        
    def __init__(self, wheel_base=2650., vehicle_width=1830):
        """ ʹ�ó��������������ʼ���˶�ģ��
        input:
          wheel_base: mm ���
          vehicle_width: mm ���
        Attribute:
          track: # distance from origin to the current position
          theta: # heading degree of vehicle
          pos: # heading degree of vehicle
        """
        self._H = 1.*wheel_base / 1000
        self._W = 1.*vehicle_width / 1000
        self.track = 0.     # distance from origin to the current position
        self.theta = 0.     # heading degree of vehicle
        self.pos = self.Point() # position of vehicle in world coordinate

    def _steeringwheel_radius(self, str_whl_angle, shft_pos):
        """ �˶��뾶����
        input:
          str_whl_angle: �����̽Ƕ�
          shft_pos: ��λ
        output:
          radius: �˶��뾶
        """
        # clk_wise
        if str_whl_angle < 0:
            radius = 2.81 / np.tan((5.955e-06*(-str_whl_angle)*(-str_whl_angle) + 0.05241*(-str_whl_angle) + 0.7268)*np.pi / 180) - 1.86 / 2
        # anti-clk_wise
        else:
            radius = 2.81 / np.tan((5.955e-06*(str_whl_angle)*(str_whl_angle) + 0.05241*(str_whl_angle) + 0.7268)*np.pi / 180) - 1.86 / 2 

        return radius
        
    def traject_predict_world(self, vhcl_can_data, time_offset):
        """ ʹ���˶�ģ�ͼ��㳵������������ϵ
        ÿ�ε��ö������ theta �� pos
        input:
          vhcl_can_data: ��ǰ֡CanLog��Ϣ
          time_offset: ������һ֡��ʱ���
        """
        shft_pos = vhcl_can_data.data["shift_pos"]
        str_whl_angle = vhcl_can_data.data["steering_angle"]
        radius = self._steeringwheel_radius(str_whl_angle, shft_pos)
        speed = (vhcl_can_data.data["wheel_speed_rl"] + vhcl_can_data.data["wheel_speed_rr"])/2
        track_offset = time_offset / 1000000.0 *speed
        track_offset /= TIME_SCALE
        
        if shft_pos == 2:
            if str_whl_angle < 0:
                theta_offset = track_offset/radius;
                x_offset = radius*(1-np.cos(np.abs(theta_offset)));
                y_offset = radius*np.sin(np.abs(theta_offset));
                self.pos.x = self.pos.x+np.cos(self.theta)*x_offset+np.sin(self.theta)*y_offset;
                self.pos.y = self.pos.y-np.sin(self.theta)*x_offset+np.cos(self.theta)*y_offset;
                self.theta += theta_offset;
            else:
                theta_offset = -track_offset/radius;
                x_offset = -radius*(1-np.cos(np.abs(theta_offset)));
                y_offset = radius*np.sin(np.abs(theta_offset));
                self.pos.x = self.pos.x+np.cos(self.theta)*x_offset+np.sin(self.theta)*y_offset;
                self.pos.y = self.pos.y-np.sin(self.theta)*x_offset+np.cos(self.theta)*y_offset;
                self.theta += theta_offset;
        else:
            if str_whl_angle<0:
                theta_offset = -track_offset/radius;
                x_offset = radius*(1-np.cos(np.abs(theta_offset)));
                y_offset = -radius*np.sin(np.abs(theta_offset));
                self.pos.x = self.pos.x+np.cos(self.theta)*x_offset+np.sin(self.theta)*y_offset;
                self.pos.y = self.pos.y-np.sin(self.theta)*x_offset+np.cos(self.theta)*y_offset;
                self.theta += theta_offset;
            else:
                theta_offset = track_offset/radius;
                x_offset = -radius*(1-np.cos(np.abs(theta_offset)));
                y_offset = -radius*np.sin(np.abs(theta_offset));
                self.pos.x = self.pos.x+np.cos(self.theta)*x_offset+np.sin(self.theta)*y_offset;
                self.pos.y = self.pos.y-np.sin(self.theta)*x_offset+np.cos(self.theta)*y_offset;
                self.theta += theta_offset;


def main():
    pass


if __name__=="__main__":
    pass
    main()

