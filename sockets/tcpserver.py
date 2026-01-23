# Python - Eisagwgh stous Ypologistes
import socket as s

serverPort = 10000

serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1) # UDP doesn't have this

while 1:
  #connectionSocket, addr = serverSocket.accept() # UDP doesn't have this (you get the clientAddress in recvfrom)
  clientSocket, _ = serverSocket.accept()
  message = clientSocket.recv(1024) # UDP: message, clientAddress = serverSocket.recvfrom(2048)
  modifiedMessage = message.upper()
  clientSocket.send(modifiedMessage) # or sendall # UDP: serverSocket.sendto(modifiedMessage, clientAddress)
  clientSocket.close()
