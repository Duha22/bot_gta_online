import socket

sock = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

sock.bind(('127.0.0.1', 10000))
sock.listen(1)
conn, addr = sock.accept()

print('connected:', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send(f"[INFO] Data = {data}".encode('utf-8'))

conn.close()