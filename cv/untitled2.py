import cv2
import multiprocessing
import threading
import time
import numpy as np

surfaces = ['RFDLUFDFR', 'FDBURBLRU', 'BRURFFFDF',
            'DBUUDBFRB', 'UDLLLUDLL', 'RLBUBBLDR']
face_number=0
grid_colors=[]
_update_flag=0
_show_select_face_flag=0

def update_surfaces():
    global _update_flag
    _update_flag=1

def show_select_face(flag):
    global _show_select_face_flag
    if flag==0 and _show_select_face_flag!=0:
        _show_select_face_flag=-1
        return
    _show_select_face_flag=flag
    
class VisionProcess(threading.Thread):
    def __init__(self):
        super(VisionProcess, self).__init__()
        self.daemon = True

    def run(self):
        cap=cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BRIGHTNESS,0.1)
#        cap.set(cv2.CAP_PROP_SATURATION,0.35)
        red_orange = 0.5  # type: int  555!
        global _update_flag
        global face_number
        global grid_colors
        global _show_select_face_flag
        while 1:
            _, image = cap.read()
            k = 25
            grids = [0] * 9
            grid_colors = [0] * 9
            grid_center = [(145, 92), (305, 92), (480, 92),
                           (145, 250), (305, 250), (480, 250),
                           (145, 390), (305, 390), (480, 390)]
            for i in range(9):
                center = grid_center[i]
                #                if i==4:
                #                    x1=center[0]-2*k
                #                    x2=center[0]+2*k
                #                    y1=center[1]-2*k
                #                    y2=center[1]+2*k
                #                else:
                x1 = center[0] - k
                x2 = center[0] + k
                y1 = center[1] - k
                y2 = center[1] + k
                grids[i] = image[y1:y2, x1:x2]
                grid = grids[i] * 1
                b = int(np.average(grid[:, :, 0]))
                g = int(np.average(grid[:, :, 1]))
                r = int(np.average(grid[:, :, 2]))
                grid[:, :] = (b, g, r)
                cvt = cv2.cvtColor(grid, cv2.COLOR_BGR2HSV)
                h = cvt[0, 0, 0]
                s = cvt[0, 0, 1]
                # v=cvt[0,0,2]
                if s < 40:
                    grids[i][:, :] = (0, 0, 0)
                    grid_colors[i] = 'D'
                else:
                    if (0 <= h < red_orange) or (165 <= h < 180):
                        grids[i][:, :] = (0, 0, 255)
                        grid_colors[i] = 'F'
                    if red_orange <= h < 25:
                        grids[i][:, :] = (204, 50, 153)
                        grid_colors[i] = 'B'
                    if 25 <= h < 60:
                        grids[i][:, :] = (0, 255, 255)
                        grid_colors[i] = 'U'
                    if 60 <= h < 100:
                        grids[i][:, :] = (0, 255, 0)
                        grid_colors[i] = 'R'
                    if 100 <= h < 165:
                        grids[i][:, :] = (255, 0, 0)
                        grid_colors[i] = 'L'
            if grid_colors[4] == 'D': face_number = 3  # white
            if grid_colors[4] == 'F': face_number = 2  # red
            if grid_colors[4] == 'B': face_number = 5  # orange
            if grid_colors[4] == 'U': face_number = 0  # yellow
            if grid_colors[4] == 'R': face_number = 1  # green
            if grid_colors[4] == 'L': face_number = 4  # blue

            if _update_flag:
                surfaces[face_number]=grid_colors
                cv2.imwrite("record_image/"+str(face_number+1)+".JPEG",image)
                _update_flag=0
            
            if _show_select_face_flag==-1:
                cv2.destroyWindow('face_record')
                _show_select_face_flag=0
            if _show_select_face_flag!=0:
                cv2.imshow('face_record',
                           cv2.imread("record_image/"+str(_show_select_face_flag)+".JPEG"))
            
            cv2.imshow('frame2', image)
            cv2.waitKey(20)


vision = VisionProcess()
vision.start()
print("vision module start working!")