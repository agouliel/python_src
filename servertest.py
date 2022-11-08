# https://stackoverflow.com/questions/27693982/python-server-with-images
from http.server import BaseHTTPRequestHandler, HTTPServer
from github import Github
import os, shutil

PORT_NUMBER = 8080

#URL = "https://raw.githubusercontent.com/agouliel/yamdl_test/main/myapp/templates/myapp/test.html"
#response = requests.get(URL)

g = Github(os.environ['PYGITHUB'])

#####################################################################

ops_manual_name = 'ops_manual.html'
ops_images = 'ops_manual_images'

def delete_ops_manual():
  try:
    os.unlink(ops_manual_name)
    shutil.rmtree(ops_images)
  except:
    pass

def download_ops_manual():
    repo = g.get_repo('ioniaman/OperationsWeb')

    delete_ops_manual()

    manual = repo.get_contents('documentation/manual/manual.html')
    open(ops_manual_name, 'xb').write(manual.decoded_content)

    images = repo.get_contents('documentation/manual/images')
    os.mkdir(ops_images)
    for i in images:
        open(f'{ops_images}/{i.name}', 'xb').write(i.decoded_content)

#####################################################################

def delete_attendance_manual():
  try:
    os.unlink('attendance_manual.html')
    shutil.rmtree('images')
  except:
    pass

def download_attendance_manual():
    attendance_repo = g.get_repo("ioniaman/AttendanceWeb")

    delete_attendance_manual()

    attendance_manual = attendance_repo.get_contents("manual/manual.html")
    open('attendance_manual.html', 'xb').write(attendance_manual.decoded_content)

    attendance_images = attendance_repo.get_contents("manual/images")
    os.mkdir('images')
    for i in attendance_images:
        open(f'images/{i.name}', 'xb').write(i.decoded_content)

#####################################################################

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        download_attendance_manual()
        download_ops_manual()
        
        #https://stackoverflow.com/questions/18346583/how-do-i-map-incoming-path-requests-when-using-httpserver
        if self.path == '/ops':
            #self.wfile.write(bytes("<b>Hello World</b>", 'utf-8'))
            self.path = ops_manual_name

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
    delete_attendance_manual()
    delete_ops_manual()
    server.socket.close()