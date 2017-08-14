#-*-coding:UTF-8-*-
'''
Created on 2017年8月14日-下午3:26:59
author: Gary-W
'''

import config_parser as cfg_parser
import cv2
import os
import numpy as np
from plot_pose import read_can_log
from dataio import get_filelist
from vehicle_model import CanMatchLog,VehicleMotion
from config_parser import TextParser
from draw_map import PosMap

class KeyPoint:
    def __init__(self, log = None):
        self.frame = 0
        self.x = 0
        self.y = 0
        self.yaw_rad = 0

        if log!=None:
            sitem = log.strip().split(" ")
            self.frame = int(sitem[0])
            self.x = float(sitem[1])
            self.y = float(sitem[2])
            self.yaw_deg = float(sitem[3])
            
    def __str__(self):
        return "%05d\tx: %3.5f\ty: %3.5f\tdeg: %3.5f" % (self.frame, self.x, self.y, self.yaw_rad)
            

def getKeyframeTable(gt_file_list):
    keypoint_table = {}
    for path in gt_file_list:
        with open(path,"r") as f:
            slog = f.readline()
            kp = KeyPoint(slog)
            keypoint_table[kp.frame] = kp

    return keypoint_table

class LocDR:
    
    def __init__(self):
        config_path = r"data/vehicle_config.cfg"
        cfgpar = cfg_parser.TextParser()
        cfg_table = cfgpar(config_path)
        self.bev_root = cfg_table["bev_root"]
        self.can_match_path = cfg_table["can_match_path"]
        self.can_dir = os.path.split(self.can_match_path)[0]
        self.img_filename = self.can_dir + r"\pose_map.jpg"
        
        gtlist = get_filelist(self.bev_root, ".txt")
        self.keypoint_table = getKeyframeTable(gtlist)
        self.can_match_logs = read_can_log(self.can_match_path)

        self.keys = sorted(self.keypoint_table.keys())
        st = self.keys[0]
        self.start_point = [self.keypoint_table[st].x,
                            self.keypoint_table[st].y,
                            self.keypoint_table[st].yaw_deg]
        
        self.start = 1001
        self.stop = 1500
        
    def insertDR(self):
        cfg_parser = TextParser()
        cfg_tabel = cfg_parser("data/vehicle_config.cfg")
        vm = VehicleMotion(cfg_tabel["wheel_base"],cfg_tabel["vehicle_width"])
        pose = []
        vm.setPosition(self.start_point[0],self.start_point[1],self.start_point[2])
        _vhcl_can_data = None
        for _i,vhcl_can_data in enumerate(self.can_match_logs):
            if _i > 0:
                times = (vhcl_can_data.data["time_stamp"] - _vhcl_can_data.data["time_stamp"]) #/ time_unit
                vm.traject_predict_world(vhcl_can_data, times)
                if vhcl_can_data.data["frameID"] in self.keys:
                    print "update %d" % vhcl_can_data.data["frameID"]
                    key_point = self.keypoint_table[vhcl_can_data.data["frameID"]]
                    vm.setPosition(key_point.x,key_point.y,key_point.yaw_deg)
                pose.append((vm.pos.x, vm.pos.y, vm.theta, vm.radius, int(vhcl_can_data.data["frameID"])))
            _vhcl_can_data =  vhcl_can_data
        return pose

    def disp_pose(self, vm_pose):
        cfg_parser = TextParser()
        cfg_tabel = cfg_parser("data/vehicle_config.cfg")
        mapper = PosMap(cfg_tabel)
        for pos in vm_pose:
            pos_x, pos_y, pos_yaw, r, id_ = pos
            if id_ >= self.start:
                mapper.mark_position(pos_x, pos_y, pos_yaw, False)
            if id_ == self.stop:
                break
        img_filename = self.can_dir + r"\pose_map.jpg"
        mapper.disp_map(img_filename)





if __name__=="__main__":
    pass
    loc_dr = LocDR()
    vm_pose = loc_dr.insertDR()
    loc_dr.disp_pose(vm_pose)
    
    
    