import numpy as np
import cv2
import sys

def  calc_homo(x1,x2):
    A = []
    b = []
    for n in zip(x1,x2):
        A.append((n[0][0], n[0][1], 1, 0, 0, 0,-n[0][0]*n[1][0], -n[1][0]*n[0][1]))
        A.append((0, 0, 0, n[0][0], n[0][1], 1, -n[0][0]*n[1][1], -n[0][1]*n[1][1]))
        b.append((n[1][0]))
        b.append((n[1][1]))
    nA = np.array(A)
    nb = np.array(b)
    Hm = np.linalg.inv(np.dot(nA.T,nA))
    hn = np.dot(nA.T,nb)
    h = np.dot(Hm,hn)
    h = np.append(h,1)
    return h.reshape([3,3])

def calc_rotate(h,K):
    R = np.dot(K.T, h)

if __name__=="__main__":
    x1 = np.load(sys.argv[1])
    x2 = np.load(sys.argv[2])
    print(x1.shape)
    print(x2.shape)
    rsc, mask = cv2.findHomography(x1,x2)
    h = calc_homo(x1,x2)
    img = cv2.imread(sys.argv[3])
    width,height,_ = img.shape
    
    dist = np.zeros((height, width),np.uint8)
    
    dis = cv2.warpPerspective(img,rsc,(height,width))
    lose = cv2.warpPerspective(img,h,(height,width))
    
    #K = np.array(([914.519, 0., 643.241],[0., 914.572, 354.503], [0., 0., 1.]))
    #K = np.array(([636.025, 0., 640.166],[0., 634.531, 368.266], [0., 0., 1.]))
    
    K = np.array(([924.088, 0., 654.112],[0., 924.88, 353.077], [0., 0., 1.]))
    val,R, t, n = cv2.decomposeHomographyMat(rsc,K)
    
    cv2.imwrite("res.png",dis)
    cv2.imwrite("lose.png",lose)
    
    print(t)
    print(R)
