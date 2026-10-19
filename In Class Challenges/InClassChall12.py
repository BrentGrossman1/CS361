import socket

s = socket.socket()

server = ('localhost', 3490)

s.connect(server)

data = s.recv(100)

str = data.decode()

print(str, end='')

while (d := s.recv(128)) != b'':
    print(d.decode(), end='')