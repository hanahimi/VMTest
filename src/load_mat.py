#-*-coding:UTF-8-*-
'''
Created on 2017年6月12日-下午1:06:17
author: Gary-W
'''
from scipy.io import loadmat
from dataio import get_filelist
import numpy as np
import os
def ppow(x,n):
    y = 1.0
    for i in range(n):
        y *= x
    return y
    
class LinearTable:
    def __init__(self, mat_path):
        name = os.path.split(mat_path)[-1][:-4]
        factkey, vrange = name.split("=")
        vl,vr = vrange.split(",")
        self.low_val = float(vl)
        self.high_val = float(vr)
        D = loadmat(mat_path)
        if factkey not in D:
            factkey = "Radius"
        self.factors = np.squeeze(D[factkey])
    
    def check(self, val):
        if self.low_val <= val <= self.high_val:
            return True
        else:
            return False
    
    def calc_radius(self, deg):
        pass
        radius = 0.
        n = len(self.factors)
        for i in range(n):
            radius += ppow(deg, n-i-1) * self.factors[i]
        return radius


def load_table():
    mat_root_dir = "mat"
    mat_path_list = get_filelist(mat_root_dir, ".mat")
    tables = []
    for mat_path in mat_path_list:
        lt = LinearTable(mat_path)
#         print lt.low_val, lt.high_val
        tables.append(lt) 
    return tables

def calc_radius(linear_table, steering_angle):
    r = 10000.
    for lt in linear_table:
        if lt.check(steering_angle):
            r = lt.calc_radius(steering_angle)
    return r

def main():
    linear_tables = load_table()
    steering_angle = 470.4
    r = calc_radius(linear_tables, steering_angle)
    print "r = ",r
    
if __name__=="__main__":
    pass
    main()






