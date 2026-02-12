# taken from Python Distilled p.286
import socket as s
import sys

if len(sys.argv) > 1:
    webserver = sys.argv[1]
else:
    webserver = 'httpforever.com'

if len(sys.argv) > 2:
    port = sys.argv[2]
else:
    port = 80

def connect(webserver, port):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((webserver, port))
    sock.send(b'GET /index.html HTTP/1.0\r\n\r\n')

    # receive data from the destination web server
    parts = []
    while True: 
        part = sock.recv(10000) # 10kb
        if not part:
            break
        parts.append(part)
        data = b''.join(parts)
    return data

if __name__ == '__main__':
    data = connect(webserver, port)
    print(data)
