#-*-coding:UTF-8-*-
'''
Created on 2017年6月12日-上午10:45:05
author: Gary-W
'''
from config_parser import TextParser
from vehicle_model import CanMatchLog,VehicleMotion, can_insert
from draw_map import PosMap
import numpy as np

def read_can_log(can_filename):
    can_match_logs = []
    with open(can_filename) as f:
        lines = f.readlines()
        for line in lines:
            _can_log = CanMatchLog(line)
            can_match_logs.append(_can_log)
    return can_match_logs


def generate_pose(can_match_logs):
    cfg_parser = TextParser()
    cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    vm = VehicleMotion(cfg_tabel["wheel_base"],cfg_tabel["vehicle_width"])
    pose = []
    _vhcl_can_data = None
    time_unit = 40000
    for _i,vhcl_can_data in enumerate(can_match_logs):
        vhcl_can_data.data["time_stamp"] /= time_unit
        vhcl_can_data.data["time_stamp"] *= time_unit
        if _i > 0:
            times = (vhcl_can_data.data["time_stamp"] - _vhcl_can_data.data["time_stamp"]) / time_unit
#             print "ori detal time = ", vhcl_can_data.data["time_stamp"] - _vhcl_can_data.data["time_stamp"]
            
            can_log_ist = can_insert(_vhcl_can_data, vhcl_can_data, times=times)
            print times, len(can_log_ist)
            print "A", _vhcl_can_data
            print "B", vhcl_can_data
            for t in range(1, len(can_log_ist)):
                print "i=",t, can_log_ist[t-1]
                time_stamp1 = can_log_ist[t-1].data["time_stamp"]
                time_stamp2 = can_log_ist[t].data["time_stamp"]
                time_offset = time_stamp2 - time_stamp1
                vm.traject_predict_world(can_log_ist[t], time_offset)
                pose.append((vm.pos.x, vm.pos.y, vm.theta, vm.radius))
        _vhcl_can_data =  vhcl_can_data

    return pose

def disp_pose(vm_pose):
    cfg_parser = TextParser()
    cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    mapper = PosMap(cfg_tabel)
    for pos in vm_pose:
        pos_x, pos_y, pos_yaw, r = pos
        mapper.mark_position(pos_x, pos_y, pos_yaw)
#         print "radius = ", r
    mapper.disp_map()

def main():
    can_filename = r"data/can_match_0519_ep21_01_v1.txt"
    can_match_logs = read_can_log (can_filename)
    vm_pose = generate_pose(can_match_logs)
    disp_pose(vm_pose)
    

if __name__=="__main__":
    pass
    main()





