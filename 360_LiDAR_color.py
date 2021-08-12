import cv2
import numpy as np
from scipy.spatial.transform import Rotation
import os
import sys
import open3d as o3d

class Camera:
    def __init__(self,cmtx,rtmtx,pos):
        self.cmtx = cmtx
        self.rtmtx = rtmtx
        self.pos = pos
        self.setup()
    
    def setup(self):
        print("set CameraParam\n {}".format(self.cmtx))
        print("set Position {}".format(self.pos))
        print(self.rmtx)
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
            pn = np.dot(prmtx, pn[:3].T)
            pn = np.hstack((pn,1.0))
            pn = np.dot(self.rtmtx, pn.T)

            pn /=pn[2]
            rs = np.dot(self.cmtx, pn.T)

            if 0 < rs[0] < w and 0 < rs[1] < h :
                r = img[int(rs[1])][int(rs[0])][2]/255
                g = img[int(rs[1])][int(rs[0])][1]/255
                b = img[int(rs[1])][int(rs[0])][0]/255
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

    #point  = read_csv(sys.argv[1])
    point = o3d.io.read_point_cloud(sys.argv[1])
    point = np.array(point.points)
    print(point.shape)

    front_cmtx = np.load(sys.argv[2])
    front_rmtx = np.load(sys.argv[3])
    front_img = cv2.imread(sys.argv[4])
    #poler_img = cv2.imread(sys.argv[5],0)
    front_camera = Camera(front_cmtx,front_rmtx,"front")
    
    front_color_point = front_camera.create_depth_img(front_img,point)
    np.savetxt("point_front.csv",front_color_point,fmt='%.5f')
    """
    back_cmtx = np.load("params/back_cmtx_01.npy")
    back_rmtx = np.load("params/back_rmtx_01.npy")
    back_img = cv2.imread(sys.argv[3])
    back_camera = Camera(back_cmtx,back_rmtx,"back")
    back_color_point = back_camera.create_depth_img(back_img,point)
    np.savetxt("back.csv",back_color_point)
    """
