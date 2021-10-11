# https://www.youtube.com/watch?v=bJOvYgSqrOs

from vidstream import *
import socket
import threading

ip_address = socket.gethostbyname(socket.gethostname())

#server = StreamingServer('192.168.0.203', 9999)
server = StreamingServer(ip_address, 9999)
t1 = threading.Thread(target=server.start_server)
t1.start()

audio_receiver = AudioReceiver(ip_address, 8888)
t2 = threading.Thread(target=audio_receiver.start_server)
t2.start()
