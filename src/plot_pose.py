#-*-coding:UTF-8-*-
'''
Created on 2017��6��12��-����10:45:05
author: Gary-W
'''
from config_parser import TextParser
from vehicle_model import CanMatchLog,VehicleMotion, can_insert
from draw_map import PosMap
import numpy as np

world_offset = {'x':0, 'y':0}
rot_table = {2090:2}

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
    for _i,vhcl_can_data in enumerate(can_match_logs):
        if _i > 0:
            times = (vhcl_can_data.data["time_stamp"] - _vhcl_can_data.data["time_stamp"]) #/ time_unit
            vm.traject_predict_world(vhcl_can_data, times)
            if vhcl_can_data.data["frameID"] in rot_table:
                vm.theta += np.deg2rad(rot_table[vhcl_can_data.data["frameID"]])
            pose.append((vm.pos.x, vm.pos.y, vm.theta, vm.radius))
#             print vhcl_can_data.strframeId, vm.pos.x, vm.pos.y
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





