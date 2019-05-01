import serial
import time
import odrive

serial_is_connected = 0
pneumatic_states = [0, 0, 0, 0, 0]
pneumatic_table = [['a', 'A'],['b', 'B'],['c', 'C'],['d','D'],['e', 'E']]
try:
    ser = serial.Serial('/dev/ttyUSB0',115200)
except Exception as error:
    print("Serial Error")
    print(error) 
else:
    serial_is_connected = 1
    print("Serial Connected")
def control_pneumatic_valve(command):
    global pneumatic_state
    if command == 'Le':
        pneumatic_states[0] = (pneumatic_states[0] + 1) % 2
    if command == 'Lc':
        pneumatic_states[1] = (pneumatic_states[1] + 1) % 2
    if command == 'Re':
        pneumatic_states[3] = (pneumatic_states[3] + 1) % 2
    if command == 'Rc':
        pneumatic_states[2] = (pneumatic_states[2] + 1) % 2
    if command == 'Rise':
        pneumatic_states[4] = 1
    if command == 'Drop':
        pneumatic_states[4] = 0

    string_to_send = '' 
    for i in range(5):
        string_to_send += pneumatic_table[i][pneumatic_states[i]]
    ser.write(string_to_send.encode()) 
    print(string_to_send)



odrive_is_connected = 0
odrv = None
odrv_angles_bias = [-2086, -2500]
odrv_angles = [0 ,0] 
def odrive_connect():
    global odrive_is_connected
    global odrv
    try:
        print('Odrive start connecting')
        odrv = odrive.find_any() 
    except Exception as error:
        print("Odrive Error")
        print(error) 
    else:
        odrv.axis0.encoder.config.use_index = True
        odrv.axis0.controller.config.vel_limit = 2 * 10000 
        odrv.axis0.trap_traj.config.vel_limit = 1 * 10000 
        odrv.axis0.trap_traj.config.accel_limit = 140 * 10000
        odrv.axis0.trap_traj.config.decel_limit = 140 * 10000
        odrv.axis0.encoder.config.use_index = True
        odrv.axis0.controller.config.vel_limit = 5 * 10000 
        odrv.axis0.trap_traj.config.vel_limit = 3 * 10000 
        #another motor
        odrv.axis1.encoder.config.use_index = True
        odrv.axis1.controller.config.vel_limit = 2 * 10000 
        odrv.axis1.trap_traj.config.vel_limit = 1 * 10000 
        odrv.axis1.trap_traj.config.accel_limit = 140 * 10000
        odrv.axis1.trap_traj.config.decel_limit = 140 * 10000
        odrv.axis1.encoder.config.use_index = True
        odrv.axis1.controller.config.vel_limit = 10 * 10000 
        odrv.axis1.trap_traj.config.vel_limit = 9 * 10000 
        #done
        odrive_is_connected = 1
        print("Odrive Connected")

def odrive_calibration(motorID):
    global ser
    global odrv
    if motorID == 0:
        ser.write('ABcd'.encode())
        odrv.axis0.requested_state = 3
        while odrv.axis0.current_state != 1:
            time.sleep(0.1)
        odrv.axis0.requested_state = 8
        odrv.axis0.controller.move_to_pos(odrv_angles_bias[0])
        time.sleep(1)
    else:
        ser.write('abCD'.encode())
        odrv.axis1.requested_state = 3
        while odrv.axis1.current_state != 1:
            time.sleep(0.1)
        odrv.axis1.requested_state = 8
        odrv.axis1.controller.move_to_pos(odrv_angles_bias[1])
        time.sleep(1)

def odrive_disable():
    odrv.axis0.requested_state = 1
    odrv.axis1.requested_state = 1
def odrive_enable():
    odrv.axis0.requested_state = 8
    odrv.axis1.requested_state = 8

def odrive_rotate(motorID, angle):
    global odrv_angles_bias,odrv_angles
    if angle == 180:
        if odrv_angles[motorID] > 2048:
            odrv_angles[motorID] -= 4096
        else:
            odrv_angles[motorID] += 4096
    if angle == 90:
        odrv_angles[motorID] += 2048
    if angle == 270:
        odrv_angles[motorID] -= 2048
    pos = odrv_angles[motorID] + odrv_angles_bias[motorID]
    if motorID == 0:
        odrv.axis0.controller.move_to_pos(pos)
    else:
        odrv.axis1.controller.move_to_pos(pos)


#ser.write('aBcDe')
def send_command(command):
    if command == 'Odrive':
        odrive_connect()
    if command == 'Cal0':
        odrive_calibration(0)
    if command == 'Cal1':
        odrive_calibration(1)

    if serial_is_connected:
        if command in ['Le', 'Lc', 'Re', 'Rc', 'Rise', 'Drop']:
            control_pneumatic_valve(command)
    else:
        print(command)
        time.sleep(1)

    if odrive_is_connected:
        if command == 'OdEn':
            odrive_enable()
        if command == 'OdDis':
            odrive_disable()
        if command in ['Od0R1', 'Od0R3', 'Od0R2', 'Od1R1', 'Od1R3', 'Od1R2']:
            odrive_rotate(int(command[2]), int(command[-1]) * 90)

