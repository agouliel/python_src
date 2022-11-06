from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import requests

URL = "https://raw.githubusercontent.com/agouliel/yamdl_test/main/myapp/templates/myapp/test.html"
response = requests.get(URL)

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        #https://stackoverflow.com/questions/18346583/how-do-i-map-incoming-path-requests-when-using-httpserver
        if self.path == '/hello':
          self.wfile.write(bytes("<b>Hello World</b>", 'utf-8'))
        elif self.path == '/file':
          self.wfile.write(response.content)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")