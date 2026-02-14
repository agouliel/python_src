# https://www.geeksforgeeks.org/python/creating-a-proxy-webserver-in-python-set-1/
# test it with: curl -x 'http://localhost:10000' 'http://httpforever.com'
import socket as s
import signal
import sys
import connect_to_site
import helpers

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
  webserver, port = helpers.extract_server_and_port(message_str)
  print('Received client request for destination:', webserver, port)
  
  # send the request to the destination
  data = connect_to_site.connect(webserver, port)

  clientSocket.send(data) # send to browser/client
  print('Sent response of the destination to the client')

  clientSocket.close()
  print('Client socket closed')
  print('----------------')
