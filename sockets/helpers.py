# https://www.geeksforgeeks.org/python/creating-a-proxy-webserver-in-python-set-1/
def extract_server_and_port(message_str):
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
  return webserver, port