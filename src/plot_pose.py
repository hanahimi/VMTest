#-*-coding:UTF-8-*-
'''
Created on 2017��6��12��-����10:45:05
author: Gary-W
'''
from config_parser import TextParser
from vehicle_model import CanMatchLog,VehicleMotion, can_insert
from draw_map import PosMap
import numpy as np

start_point = [0,0,0] # xm,ym, deg
rot_table = {}

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
    vm.setPosition(start_point[0],start_point[1],start_point[2])
    _vhcl_can_data = None
    for _i,vhcl_can_data in enumerate(can_match_logs):
        if _i > 0:
            times = (vhcl_can_data.data["time_stamp"] - _vhcl_can_data.data["time_stamp"]) #/ time_unit
            vm.traject_predict_world(vhcl_can_data, times)
            if vhcl_can_data.data["frameID"] in rot_table:
                vm.theta += np.deg2rad(rot_table[vhcl_can_data.data["frameID"]])
            pose.append((vm.pos.x, vm.pos.y, vm.theta, vm.radius, _i))
#             print vhcl_can_data.strframeId, vm.pos.x, vm.pos.y
        _vhcl_can_data =  vhcl_can_data
    return pose

def disp_pose(vm_pose):
    cfg_parser = TextParser()
    cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    mapper = PosMap(cfg_tabel)
    for pos in vm_pose:
        pos_x, pos_y, pos_yaw, r, id_ = pos
        mapper.mark_position(pos_x, pos_y, pos_yaw)
        print pos_x, pos_y, pos_yaw
    mapper.disp_map()

def save_pose(pos_filename, vm_pose):
    cfg_parser = TextParser()
    cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    with open(pos_filename, "w") as f:
        for i, pose in enumerate(vm_pose):
            a = np.cos(pose[2])
            b = np.sin(pose[2])
            t = np.arccos(a) if b > 0 else -np.arccos(a)
            msg = "%05d %f %f %f\n" % ( pose[4], pose[0],pose[1],t)
            f.write(msg)

def main():
    can_filename = r"data/can_match_0606_ep21_01_v1.txt"
    can_match_logs = read_can_log (can_filename)
    vm_pose = generate_pose(can_match_logs)
    disp_pose(vm_pose)
    pos_filename = can_filename[:-4]+"_pos.txt"
    save_pose(pos_filename, vm_pose)    

if __name__=="__main__":
    pass
    main()





