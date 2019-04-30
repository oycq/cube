import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8080))
s.sendall(('FUDRULRBFUFLRRUBDFBLRLFBRRLUDUFDLFDLLUDDLUDRBBBUFBFDBR'+'\n').encode())
print(s.recv(2048).decode())
s.close()
#BURUUDDLLDFFURLRRLLBBRFLLRDBFBLDUFDFRBFRLBRDUDFUFBDUBU