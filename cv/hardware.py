import serial
import time
import odrive
import os

serial_is_connected = 0
pneumatic_states = [0, 0, 0, 0, 0]
pneumatic_table = [['a', 'A'],['b', 'B'],['c', 'C'],['d','D'],['e', 'E']]
last_rotate_states = 'abcd'
try:
    ser = serial.Serial('/dev/ttyUSB0',115200)
except Exception as error:
    print("Serial Error")
    print(error) 
else:
    serial_is_connected = 1
    print("Serial Connected")
def control_pneumatic_valve(command):
    global pneumatic_states
    global last_rotate_states
    for i in range(4):
        if last_rotate_states[i] == chr(ord('a') + i):
            pneumatic_states[i] = 0
        else:
            pneumatic_states[i] = 1
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
    last_rotate_states = string_to_send[:4] 
    if serial_is_connected:
        ser.write(string_to_send.encode()) 
    print(string_to_send)


base_accel = 140
ex_accel = 140
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
        odrv.axis0.trap_traj.config.accel_limit = base_accel * 10000
        odrv.axis0.trap_traj.config.decel_limit = base_accel * 10000
        odrv.axis0.encoder.config.use_index = True
        odrv.axis0.controller.config.vel_limit = 5 * 10000 
        odrv.axis0.trap_traj.config.vel_limit = 3 * 10000 
        #another motor
        odrv.axis1.encoder.config.use_index = True
        odrv.axis1.controller.config.vel_limit = 2 * 10000 
        odrv.axis1.trap_traj.config.vel_limit = 1 * 10000 
        odrv.axis1.trap_traj.config.accel_limit = base_accel * 10000
        odrv.axis1.trap_traj.config.decel_limit = base_accel * 10000
        odrv.axis1.encoder.config.use_index = True
        odrv.axis1.controller.config.vel_limit = 10 * 10000 
        odrv.axis1.trap_traj.config.vel_limit = 9 * 10000 
        #done
        odrive_is_connected = 1
        print("Odrive Connected")

odrive_connect()

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

def check_based_position():
    if abs(odrv.axis0.encoder.pos_estimate - odrv_angles_bias[0]) >90 or abs(odrv.axis1.encoder.pos_estimate - odrv_angles_bias[1]) > 90: 
            print('Not start at based postion!')
            os.abort()

def odrive_rotate(motorID, angle):
    global odrv_angles_bias,odrv_angles
    delta_range = 30
    achieve_count = -5
    if angle == 180:
        odrv_angles[motorID] += 4096
    if angle == -180:
        odrv_angles[motorID] -= 4096
    if angle == 90:
        odrv_angles[motorID] += 2048
    if angle == 270:
        odrv_angles[motorID] -= 2048
    if angle == -90:
        odrv_angles[motorID] -= 2048
    pos = odrv_angles[motorID] + odrv_angles_bias[motorID]
    if motorID == 0:
        odrv.axis0.controller.move_to_pos(pos)
    else:
        odrv.axis1.controller.move_to_pos(pos)
    for i in range(500):
        if motorID == 0:
            pos_estimate = odrv.axis0.encoder.pos_estimate
        else:
            pos_estimate = odrv.axis1.encoder.pos_estimate
        delta = abs(pos_estimate - pos)
        if delta < delta_range:
            achieve_count += 1
        if achieve_count >=0:
            break
        if i > 100:
            odrv.axis0.requested_state = 1
            odrv.axis1.requested_state = 1
            print('Can not move to expect position, Be careful!')
            os.abort()
        #print('0:  %7.1f   1:  %7.1f'%(odrv_angles[0],odrv_angles[1]))
        print('%4d  %4d  %5.2f   %5.2f'%(i,motorID,odrv_angles[motorID],delta))
        time.sleep(0.001)

    odrv.axis0.trap_traj.config.accel_limit = base_accel * 10000
    odrv.axis0.trap_traj.config.accel_limit = base_accel * 10000

def cubic_rotate(command):
    print(command)
    global last_rotate_states
    delay_time = 0.035
    clamp_time = 0.080 - delay_time 
    release_time = 0.080
    dict = {
            'L3': ['AbCD', ( 0 ,  90), 'ABcd', ( 0 , -90)],
            'R3': ['ABCd', ( 0 ,  90), 'ABcd', ( 0 , -90)],
            'U3': ['ABcD', ( 90,  0 ), 'abCD', (-90,  0 )],
            'D3': ['aBCD', ( 90 , 0 ), 'abCD', (-90,  0 )],
            'F3': ['abCD', ( 0 ,  90), 'ABcd', ( 0 , -90),
                   'aBCD', ( 90 , 0 ), 'abCD', (-90,  0 )],
            'B3': ['ABcd', ( 90 , 0 ), 'abCD', (-90,  0 ),
                   'ABCd', ( 0  , 90), 'ABcd', ( 0 , -90)],
            'L1': ['AbCD', ( 0 , -90), 'ABcd', ( 0 ,  90)],
            'R1': ['ABCd', ( 0 , -90), 'ABcd', ( 0 , +90)],
            'U1': ['ABcD', (-90,  0 ), 'abCD', (+90,  0 )],
            'D1': ['aBCD', (-90 , 0 ), 'abCD', (+90,  0 )],
            'F1': ['abCD', ( 0 ,  90), 'ABcd', ( 0 , -90),
                   'aBCD', (-90 , 0 ), 'abCD', (+90,  0 )],
            'B1': ['ABcd', ( 90 , 0 ), 'abCD', (-90,  0 ),
                   'ABCd', ( 0  ,-90), 'ABcd', ( 0 , +90)],
            'L2': ['AbCD', ( 0 , -180), 'AbCd' ,'ABcd', ( 0 , 180)],
            'R2': ['ABCd', ( 0 , -180), 'ABcd', ( 0 , 180)],
            'U2': ['ABcD', (180,  0  ), 'aBcD','abCD', (-180,  0 )],
            'D2': ['aBCD', (180 , 0  ), 'abCD', (-180,  0 )],
            'F2': ['abCD', ( 0 ,  90 ), 'ABcd', ( 0 , -90),
                   'aBCD', (180 , 0  ), 'abCD', (-180,  0 )],
            'B2': ['ABcd', ( 90 , 0 ), 'abCD', (-90,  0 ),
                   'ABCd', ( 0  ,-180), 'ABcd', ( 0 , 180)]


             }
    if odrive_is_connected:
        check_based_position()
    for item in dict[command]: 
        if isinstance(item, str):
            if abs(ord(item[0]) - ord(item[1])) < 5:
                if abs(ord(item[2]) - ord(item[3])) < 5:
                    odrv.axis0.trap_traj.config.accel_limit = ex_accel * 10000
                    odrv.axis1.trap_traj.config.accel_limit = ex_accel * 10000
 
            print(last_rotate_states, item)
            string_to_send = ''
            if last_rotate_states == 'abcd':
                last_rotate_states = ''
                for i in range(4):
                    if item[i] == chr(ord('a') + i):
                        last_rotate_states += chr(ord('A') + i)
                    else:
                        last_rotate_states += chr(ord('a') + i)
            for i in range(4):
                if last_rotate_states[i] > item[i]:
                    string_to_send += item[i]
            if len(string_to_send):
                if serial_is_connected:
                    ser.write(string_to_send.encode())
                    print('ser:  '+string_to_send)
                else:
                    print(string_to_send)
                time.sleep(clamp_time)
            string_to_send = ''
            for i in range(4):
                if last_rotate_states[i] < item[i]:
                    string_to_send += item[i]
            if len(string_to_send):
                if serial_is_connected:
                    ser.write(string_to_send.encode())
                    print('ser:  '+string_to_send)
                else:
                    print(string_to_send)
                time.sleep(release_time)
            else:
                time.sleep(delay_time)
            last_rotate_states = item
        else:
            if odrive_is_connected and serial_is_connected:
                if item[0] != 0:
                    odrive_rotate(0 ,item[0])
                if item[1] != 0:
                    odrive_rotate(1 ,item[1])
            else:
                print(item)
                time.sleep(1)

def send_command(command):
    if command == 'Odrive':
        odrive_connect()
    if command == 'Cal0':
        odrive_calibration(0)
    if command == 'Cal1':
        odrive_calibration(1)

    if command in ['Le', 'Lc', 'Re', 'Rc', 'Rise', 'Drop']:
        control_pneumatic_valve(command)

    if odrive_is_connected:
        if command == 'OdEn':
            odrive_enable()
        if command == 'OdDis':
            odrive_disable()
        if command in ['Od0R1', 'Od0R3', 'Od0R2', 'Od1R1', 'Od1R3', 'Od1R2']:
            odrive_rotate(int(command[2]), int(command[-1]) * 90)
    if command in ['L1','L2','L3','R1','R2','R3','U1','U2','U3','D1','D2','D3','F1','F2','F3','B1','B2','B3']:
        cubic_rotate(command)

