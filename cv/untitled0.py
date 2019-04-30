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

def update_surfaces():
    global _update_flag
    _update_flag=1

class VisionProcess(multiprocessing.Process):
    def __init__(self):
        super(VisionProcess,self).__init__()
        self.daemon=True      
        self.pipe=multiprocessing.Pipe()      
        t=threading.Thread(target=self.pipe_receive_thread)
        t.daemon=True
        t.start()
    def run(self):
        cap=cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_BRIGHTNESS,0.3)
        cap.set(cv2.CAP_PROP_SATURATION,0.18)
        while(1):
            _,image=cap.read()
#            _,image1=cap.read()
#            _,image2=cap.read()
#            image=image1/2+image2/2
            k=25
            grids=[0]*9
            grid_colors=[0]*9
            grid_center = [(145, 92), (305, 92), (480, 92),
                           (145, 250), (305, 250), (480, 250),
                           (145, 390), (305, 390), (480, 390)]
            for i in range(9):
                center=grid_center[i]
                x1=center[0]-k
                x2=center[0]+k
                y1=center[1]-k
                y2=center[1]+k 
                grids[i]=image[y1:y2,x1:x2]
                grid=grids[i]*1
                b=int(np.average(grid[:,:,0]))
                g=int(np.average(grid[:,:,1]))
                r=int(np.average(grid[:,:,2]))
                red_flag=0
                green_flag=0
                white_flag=0
                if b+g<=10:
                    red_flag=1
                if r<10:
                    green_flag=1
                if min([r,g,b])/(max([r,g,b])+0.01)>0.8:
                    white_flag=1
                grid[:,:]=(b,g,r)
                cvt=cv2.cvtColor(grid, cv2.COLOR_BGR2HSV)
                h=cvt[0,0,0]
                s=cvt[0,0,1]
                # v=cvt[0,0,2]
                if (white_flag):
                    grids[i][:,:]=(0,0,0)
                    grid_colors[i]='D'       
                else:
                    if (h>=0 and h<25) or (h>=165 and h<180):
                        if red_flag:
                            grids[i][:,:]=(0,0,255)
                            grid_colors[i]='F'
                        else:
                            grids[i][:,:]=(0,130,255)
                            grid_colors[i]='B'
                    if h>=25 and h<100:
                        if green_flag:
                            grids[i][:,:]=(0,255,0)
                            grid_colors[i]='R'
                        else:
                            grids[i][:,:]=(0,255,255)
                            grid_colors[i]='U'
                    if h>=100 and h<165:
                        grids[i][:,:]=(255,0,0)
                        grid_colors[i]='L'
            if grid_colors[4]=='D': face_number=3#white
            if grid_colors[4]=='F': face_number=2#red
            if grid_colors[4]=='B': face_number=5#orange
            if grid_colors[4]=='U': face_number=0#yellow
            if grid_colors[4]=='R': face_number=1#green
            if grid_colors[4]=='L': face_number=4#blue

            self.pipe[0].send((face_number,grid_colors))

            cv2.imshow('frame2',image)
            cv2.waitKey(20)
    
    def pipe_receive_thread(self):
        global face_number,grid_colors
        global _update_flag
        while(1):
            face_number,grid_colors=self.pipe[1].recv()
            if _update_flag:
                surfaces[face_number] = grid_colors
                cv2.imwrite(str(face_number)+'.JPGE',image)
            
vision=VisionProcess()
vision.start()
#time.sleep(1.5)
print("vision module start working!")
if __name__=='__main__':
    while(1):
        print(face_number,grid_colors)
        time.sleep(0.02)z