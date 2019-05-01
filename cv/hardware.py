import serial
import time

is_connected = 0
try:
    ser = serial.Serial('/dev/ttyUSB0',115200)
except StandardError as error:
    print(error) 
else:
    is_connected = 1
    print("Serial Connected")

pneumatic_states = [0, 0, 0, 0, 0]
pneumatic_table = [['a', 'A'],['b', 'B'],['c', 'C'],['d','D'],['e', 'E']]

def control_pneumatic_valve(command):
    global pneumatic_state
    if command == 'Le':
        pneumatic_states[0] = (pneumatic_states[0] + 1) % 2
    if command == 'Lc':
        pneumatic_states[1] = (pneumatic_states[1] + 1) % 2
    if command == 'Re':
        pneumatic_states[2] = (pneumatic_states[2] + 1) % 2
    if command == 'Rc':
        pneumatic_states[3] = (pneumatic_states[3] + 1) % 2
    if command == 'Rise':
        pneumatic_states[4] = 0
    if command == 'Drop':
        pneumatic_states[4] = 1
    string_to_send = '' 
    for i in range(5):
        string_to_send += pneumatic_table[i][pneumatic_states[i]]
    ser.write(string_to_send.encode()) 
    print(string_to_send)

#ser.write('aBcDe')
def send_command(command):
    if is_connected:
        if command == 'Le' or 'Lc' or 'Re' or 'Rc' or 'Rise' or 'Drop':
            control_pneumatic_valve(command)
    else:
        print(command)
        time.sleep(1)
