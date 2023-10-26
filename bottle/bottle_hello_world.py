from bottle import route, run, template, get

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

# https://adamo.wordpress.com/2021/10/06/return-a-blank-favicon-ico-with-python-bottle/
@get('/favicon.ico')
def get_favicon():
    #response.content_type = 'image/x-icon'
    return "data:image/x-icon;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQEAYAAABPYyMiAAAABmJLR0T///////8JWPfcAAAACXBIWXMAAABIAAAASABGyWs+AAAAF0lEQVRIx2NgGAWjYBSMglEwCkbBSAcACBAAAeaR9cIAAAAASUVORK5CYII="

run(host='localhost', port=8080)

