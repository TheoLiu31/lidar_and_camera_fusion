import cv2
import numpy as np
from scipy.spatial.transform import Rotation
import os
import sys

class Camera:
    def __init__(self,cmtx,pos):
        self.cmtx = cmtx
        self.pos = pos
        self.setup()
    
    def setup(self):
        print("set CameraParam\n {}".format(self.cmtx))
        print("set Position {}".format(self.pos))

    def create_depth_img(self,h,w,point):
        img =  np.zeros((h,w,3))
        print("create_depth_img")
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
            if(pn[2] < 0.0):
                continue
            pn /=pn[2]
            rs = np.dot(self.cmtx, pn.T)
            if 0 < rs[0] < w and 0 < rs[1] < h and pt[2] < 100 and pt[3] > 0:
                img[int(rs[1])][int(rs[0])][0] = int(pt[3]/100*255)
                img[int(rs[1])][int(rs[0])][1] = int(pt[3]/100*255)
                img[int(rs[1])][int(rs[0])][2] = int(pt[3]/100*255)
    
        img = img.astype(np.uint8)
        cv2.imwrite("{}.png".format(self.pos), img)

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
    
    cmtx = np.load("params/front_cmtx.npy")
    front_camera = Camera(cmtx,"front")
    front_camera.create_depth_img(720,1280,point)

    right_camera = Camera(cmtx,"right")
    right_camera.create_depth_img(720,1280,point)

    left_camera = Camera(cmtx,"left")
    left_camera.create_depth_img(720,1280,point)
    
    back_camera = Camera(cmtx,"back")
    back_camera.create_depth_img(720,1280,point)