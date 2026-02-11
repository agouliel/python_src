# https://www.geeksforgeeks.org/python/creating-a-proxy-webserver-in-python-set-1/
# test it with: curl -x 'http://localhost:10000' 'http://httpforever.com'
import socket as s
import signal
import sys

serverPort = 10000

serverSocket = s.socket(s.AF_INET, s.SOCK_STREAM)
# https://stackoverflow.com/questions/6380057/address-already-in-use-error-when-binding-a-socket-in-python
serverSocket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

# https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python
def signal_handler(sig, frame):
    serverSocket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print('Proxy running...')

while 1:
  # "client" is the client of the proxy, for example browser or curl
  clientSocket, _ = serverSocket.accept()
  request = clientSocket.recv(1024)
  message_str = request.decode()
  first_line = message_str.split('\n')[0]
  url = first_line.split(' ')[1]
  http_pos = url.find("://") # find pos of ://
  if (http_pos==-1):
      temp = url
  else:
      temp = url[(http_pos+3):] # get the rest of url

  port_pos = temp.find(":") # find the port pos (if any)

  # find end of web server
  webserver_pos = temp.find("/")
  if webserver_pos == -1:
      webserver_pos = len(temp)

  webserver = ""
  port = -1
  if (port_pos==-1 or webserver_pos < port_pos):
      # default port 
      port = 80 
      webserver = temp[:webserver_pos]
  else: # specific port 
      port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
      webserver = temp[:port_pos]
  print('Received client request for destination:', webserver, port)
  
  # send the request to the destination
  sock = s.socket(s.AF_INET, s.SOCK_STREAM) 
  sock.connect((webserver, port))
  sock.sendall(request)
  print('Sent the client request to the destination')

  # receive data from the destination web server
  data = sock.recv(20000) # 20kb
  clientSocket.send(data) # send to browser/client
  print('Sent response of the destination to the client')

  clientSocket.close()
  print('Client socket closed')
  print('----------------')
