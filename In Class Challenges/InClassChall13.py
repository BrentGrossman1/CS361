import socket
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(("localhost", 3490))

s.listen()

while True:
    client_socket, client_addr = s.accept()
    print(client_addr)
    client_socket.sendall("Some data!\n".encode())
    client_socket.close()