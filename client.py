import socket

sock = socket.socket()
sock.connect(('localhost', 5555))
text = input(">>> ")
sock.send(text)

data = sock.recv(1024)
sock.close()

print(data)