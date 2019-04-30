import bluetooth
import time

is_connected = True
try:
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # client_socket.connect(("98:D3:31:FB:11:4D", 1))
    #client_socket.connect(("00:21:13:00:CD:C0", 1))
    client_socket.connect(("00:21:13:00:B2:DF", 1))

except StandardError:
    pass
print("BlueTooth Connected")


def send_command(command):
    if is_connected:
        if command == '+' or command == '-':
            client_socket.send(command)
            client_socket.recv(1024)
            time.sleep(0.02)
        else:
            if command == 7:
                client_socket.send('7')
                client_socket.recv(1024)
                #ime.sleep(1.5)
            else:
                client_socket.send(str(command))
                client_socket.recv(1)
                #time.sleep(1)
    else:
        print(command)
        time.sleep(1)
