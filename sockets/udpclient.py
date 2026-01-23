# Python - Eisagwgh stous Ypologistes
import socket as s

serverName = '127.0.0.1'
serverPort = 10000

clientSocket = s.socket(s.AF_INET, s.SOCK_DGRAM)

message = 'test'

clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)

clientSocket.close()
