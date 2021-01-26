import numpy as np
import cv2
import sys

class PointList():
    def __init__(self,savename):
        self.ptlist = []
        self.pos = 0
        self.name = savename

    def add(self, x, y):
        self.ptlist.append([x,y,1])
        self.pos += 1
    
    def save(self):
        print(self.ptlist)
        np.save(self.name,np.array(self.ptlist))
    def remove(self):
        x, y, _ =self.ptlist.pop(-1)
        self.pos -=1
        return x, y

def onMouse(event, x, y, flag, params):
    wname, img, ptlist = params
    if event == cv2.EVENT_MOUSEMOVE:
        img2 = np.copy(img)
        h, w = img2.shape[0], img2.shape[1]
        cv2.line(img2, (x, 0), (x, h - 1), (255, 0, 0))
        cv2.line(img2, (0, y), (w - 1, y), (255, 0, 0))
        cv2.imshow(wname, img2)

    if event == cv2.EVENT_LBUTTONUP:
        ptlist.add(x, y)
        print('[%d] ( %d, %d )' % (ptlist.pos - 1, x, y))
        cv2.circle(img, (x, y), 3, (0, 0, 255), 1)
        cv2.imshow(wname, img)
    if event == cv2.EVENT_MBUTTONUP:
        x, y = ptlist.remove()
        cv2.circle(img, (x, y), 3, (0, 0, 0), 1)
        cv2.imshow(wname, img)
    if event == cv2.EVENT_RBUTTONDOWN:
        print("save_point")
        ptlist.save()

if __name__ == '__main__':
    
    img = cv2.imread("{}".format(sys.argv[1]))
    wname = "MouseEvent"
    cv2.namedWindow(wname)
    ptlist = PointList(sys.argv[2])
    cv2.namedWindow(wname, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(wname, onMouse, [wname, img, ptlist])
    cv2.imshow(wname, img)
    cv2.waitKey()
    cv2.destroyAllWindows()