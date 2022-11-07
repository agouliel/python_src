from http.server import BaseHTTPRequestHandler, HTTPServer
from github import Github
import os, shutil

PORT_NUMBER = 8080

#URL = "https://raw.githubusercontent.com/agouliel/yamdl_test/main/myapp/templates/myapp/test.html"
#response = requests.get(URL)

g = Github(os.environ['PYGITHUB'])

def download_attendance_manual():
    attendance_repo = g.get_repo("ioniaman/AttendanceWeb")

    attendance_manual = attendance_repo.get_contents("manual/manual.html")
    try: os.unlink('attendance_manual.html')
    except: pass
    open('attendance_manual.html', 'xb').write(attendance_manual.decoded_content)

    attendance_images = attendance_repo.get_contents("manual/images")
    try: shutil.rmtree('images')
    except: pass
    os.mkdir('images')
    #os.chdir('images')
    for i in attendance_images:
        open(f'images/{i.name}', 'xb').write(i.decoded_content)

class myHandler(BaseHTTPRequestHandler):

    # https://stackoverflow.com/questions/27693982/python-server-with-images
    def do_GET(self):
        download_attendance_manual()
        
        #https://stackoverflow.com/questions/18346583/how-do-i-map-incoming-path-requests-when-using-httpserver
        if self.path == '/hello':
            #self.wfile.write(bytes("<b>Hello World</b>", 'utf-8'))
            self.path = 'hello.html'

        if self.path=="/attendance":
            self.path = 'attendance_manual.html'

        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg") or self.path.endswith(".jpeg"):
                mimetype='image/jpg'
                sendReply = True

            if sendReply == True:
                f = open(os.curdir+os.sep+self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started server on port:' , PORT_NUMBER)
    server.serve_forever()

except KeyboardInterrupt:
    print('Shutting down the server')
    os.unlink('attendance_manual.html')
    shutil.rmtree('images')
    server.socket.close()