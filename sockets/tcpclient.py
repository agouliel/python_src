# Python - Eisagwgh stous Ypologistes
import socket as s

serverName = '127.0.0.1'
serverPort = 10000

clientSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
clientSocket.connect((serverName, serverPort)) # UDP doesn't have this

message = 'test'

clientSocket.send(message.encode('utf-8')) # UDP: clientSocket.sendto(message.encode('utf-8'), (serverName, serverPort))

modifiedMessage = clientSocket.recv(1024) # UDP: modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage)

clientSocket.close()
