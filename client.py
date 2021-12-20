import socket

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
sock.connect(('127.0.0.1', 1235))
while True:
    text = input(">>> ")
    sock.send(text)
    data = sock.recv(1024)
    print(data.decode('utf-8'))

sock.close()

