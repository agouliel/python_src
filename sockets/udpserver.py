# Python - Eisagwgh stous Ypologistes
import socket as s

serverPort = 10000

serverSocket = s.socket(s.AF_INET, s.SOCK_DGRAM)
serverSocket.bind(('', serverPort))

while 1:
  message, clientAddress = serverSocket.recvfrom(2048)
  modifiedMessage = message.upper()
  serverSocket.sendto(modifiedMessage, clientAddress)
