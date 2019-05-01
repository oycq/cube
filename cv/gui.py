# encoding=utf-8
import start_solver
import vision
import Tkinter as tk
import time
import mission
import plan
#import blue
import threading


def manually_confirm_surface_A():
    vision.update_surfaces_A()

def manually_confirm_surface_B():
    vision.update_surfaces_B()

def manually_confirm_surface():
    vision.update_surfaces()

def execute():
    if not plan.surfaces_2_plan(vision.surfaces):
        return
    mission.add(plan.hardware_plan+['8'])


def scan_surfaces():
    vision.update_surfaces()
    blue.send_command(9)
    blue.send_command(7)
    blue.send_command(8)
    time.sleep(0.3)
    for i in range(4):
        time.sleep(0.15)
        vision.update_surfaces()
        blue.send_command(1)
    blue.send_command(9)
    blue.send_command(7)
    blue.send_command(8)
    time.sleep(0.3)
    vision.update_surfaces()
    blue.send_command(9)

def ShowTime():
    scan_surfaces()
    execute()

def pressKey(event):
    if len(event.char)==0:
        return
    key=ord(event.char)
    if key==13:#'\n'
        ShowTime()
    if key==32:#' '
        mission.end()
    if ord('0')<=key<=ord('6'):
        vision.show_select_face(key-ord('0'))

root = tk.Tk(className='cube solver')

root.bind('<Control-Alt-Shift-Up>',lambda event: mission.add(['Rise']))
root.bind('<Control-Alt-Shift-Down>',lambda event: mission.add(['Drop']))
root.bind('<Control-Up>',lambda event: mission.add(['Le']))
root.bind('<Control-Down>',lambda event: mission.add(['Lc'])) 
root.bind('<Alt-Up>',lambda event: mission.add(['Re'])) 
root.bind('<Alt-Down>',lambda event: mission.add(['Rc'])) 

root.bind('<Alt-u>',lambda event: mission.add(['U']))
root.bind('<Control-u>',lambda event: mission.add(['U\''])) 
root.bind('<Alt-Control-u>',lambda event: mission.add(['U\'\''])) 

root.bind('<Alt-d>',lambda event: mission.add(['D']))
root.bind('<Control-d>',lambda event: mission.add(['D\''])) 
root.bind('<Alt-Control-d>',lambda event: mission.add(['D\'\''])) 

root.bind('<Alt-l>',lambda event: mission.add(['L']))
root.bind('<Control-l>',lambda event: mission.add(['L\''])) 
root.bind('<Alt-Control-l>',lambda event: mission.add(['L\'\''])) 

root.bind('<Alt-r>',lambda event: mission.add(['R']))
root.bind('<Control-r>',lambda event: mission.add(['R\''])) 
root.bind('<Alt-Control-r>',lambda event: mission.add(['R\'\''])) 

root.bind('<Alt-b>',lambda event: mission.add(['B']))
root.bind('<Control-b>',lambda event: mission.add(['B\''])) 
root.bind('<Alt-Control-b>',lambda event: mission.add(['B\'\''])) 

root.bind('<Alt-f>',lambda event: mission.add(['F']))
root.bind('<Control-f>',lambda event: mission.add(['F\''])) 
root.bind('<Alt-Control-f>',lambda event: mission.add(['F\'\''])) 


temp = tk.Button(root, text='+', command=lambda: mission.add(['+']), width=10)
temp.grid(row=0, column=0, columnspan=1)  # +

temp = tk.Button(root, text='-', command=lambda: mission.add(['-']), width=10)
temp.grid(row=0, column=2, columnspan=1)  # -

temp = tk.Button(root, text='up', command=lambda: mission.add([8]), width=10)
temp.grid(row=0, column=1, columnspan=1)

temp = tk.Button(root, text='left', command=lambda: mission.add([6]), width=10)
temp.grid(row=1, column=0, columnspan=1)

temp = tk.Button(root, text='right', command=lambda: mission.add([4]), width=10)
temp.grid(row=1, column=2, columnspan=1)

temp = tk.Button(root, text='down', command=lambda: mission.add([9]), width=10)
temp.grid(row=2, column=1, columnspan=1)

temp = tk.Button(root, text='flip', command=lambda: mission.add([7]), width=10)
temp.grid(row=1, column=1, columnspan=1)

temp = tk.Button(root, text='<-', command=lambda: mission.add([3]), width=10)
temp.grid(row=2, column=0, columnspan=1)

temp = tk.Button(root, text='->', command=lambda: mission.add([1]), width=10)
temp.grid(row=2, column=2, columnspan=1)

temp = tk.Button(root, text='A', command=manually_confirm_surface_A, width=10)
temp.grid(row=3, column=0, columnspan=1)

temp = tk.Button(root, text='manually comfirm', command=manually_confirm_surface, width=10)
temp.grid(row=3, column=1, columnspan=1)

temp = tk.Button(root, text='B', command=manually_confirm_surface_B, width=10)
temp.grid(row=3, column=2, columnspan=1)

temp = tk.Button(root, text='scan', command=scan_surfaces, width=30)
temp.grid(row=4, column=0, columnspan=3)

temp = tk.Button(root, text='execute', command=lambda: execute(), width=30)
temp.grid(row=5, column=0, columnspan=3)

temp = tk.Button(root, text='ShowTime', command=lambda: ShowTime(), width=30)
temp.grid(row=6, column=0, columnspan=3)

temp = tk.Button(root, text='continue', command=lambda: mission.start(), width=10)
temp.grid(row=7, column=0, columnspan=1)

temp = tk.Button(root, text='suspend', command=lambda: mission.suspend(), width=10)
temp.grid(row=7, column=1, columnspan=1)

temp = tk.Button(root, text='end', command=lambda: mission.end(), width=10)
temp.grid(row=7, column=2, columnspan=1)

temp = tk.Button(root, text='exit', command=lambda: root.destroy(), width=30)
temp.grid(row=8, column=0, columnspan=3)

queue_label = tk.Label(root, text=' ', width=30,wraplength=200, justify = 'left')
queue_label.grid(row=9, column=0, columnspan=3, rowspan=3)


def update_queue_label():
    while True:
        queue_label['text'] = 'hardware<< '+mission.get_queue()
        time.sleep(0.03)


queue_t = threading.Thread(target=update_queue_label)
queue_t.daemon = True
queue_t.start()
root.mainloop()

if __name__ == '__main__':
    pass
