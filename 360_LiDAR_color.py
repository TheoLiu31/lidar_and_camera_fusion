import cv2
import numpy as np
from scipy.spatial.transform import Rotation
import os
import sys

class Camera:
    def __init__(self,cmtx,rmtx,pos):
        self.cmtx = cmtx
        self.rmtx = rmtx[0:3,0:3]
        self.tmtx = rmtx[0:3,3]
        self.pos = pos
        self.setup()
    
    def setup(self):
        print("set CameraParam\n {}".format(self.cmtx))
        print("set Position {}".format(self.pos))

    def create_depth_img(self,img,point):
        h, w, _ = img.shape
        color_point =[]
        print("Lidar_fusion")
        if(self.pos == "front"):
            prmtx = self._rotate_pos(0)
        elif (self.pos == "right"):
            prmtx = self._rotate_pos(-90)
        elif(self.pos == "left"):
            prmtx = self._rotate_pos(90)
        else:
            prmtx = self._rotate_pos(180)
        
        for pt in point:
            pn = np.array(pt[:3])
            pn = np.dot(prmtx, pn.T)
            pn = np.dot(self.rmtx, pn.T)
            
            pp = np.copy(pn)
            if(pn[2] < 0.0):
                continue
            pn /=pn[2]
            rs = np.dot(self.cmtx, pn.T)

            if 0 < rs[0] < w and 0 < rs[1] < h :
                r = img[int(rs[1])][int(rs[0])][2]
                g = img[int(rs[1])][int(rs[0])][1]
                b = img[int(rs[1])][int(rs[0])][0]
                color_point.append([pt[2],-pt[0],-pt[1],r,g,b])
        return color_point
    def _rotate_pos(self,deg):
        rad = np.radians(deg)
        rvec = np.array([0.0, rad, 0.0])
        rot = Rotation.from_rotvec(rvec)
        return rot.as_matrix()

def read_csv(filepath):
    lidar = []
    with open(filepath,'r') as f:
        line = f.readline().strip()
        while line:
            linestr = line.split(" ")
            lis = []
            if len(linestr) >= 4:
                lis.append(linestr[1])
                lis.append(linestr[2])
                lis.append(linestr[0])
                lis.append(linestr[3])
                linestr_convert = list(map(float, lis))
                linestr_convert[0] = - linestr_convert[0] 
                linestr_convert[1] = - linestr_convert[1] 
                lidar.append(linestr_convert)
            line = f.readline().strip()
    return np.array(lidar)

if __name__=="__main__":
    print("test")
    point  = read_csv(sys.argv[1])
    print(point.shape)

    front_cmtx = np.load("params/front_cmtx.npy")
    front_rmtx = np.load("params/front_rmtx.npy")
    front_img = cv2.imread(sys.argv[2])
    front_camera = Camera(front_cmtx,front_rmtx,"front")
    front_color_point = front_camera.create_depth_img(front_img,point)
    np.savetxt("front.csv",front_color_point)