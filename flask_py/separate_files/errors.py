from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from models import app

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message):
    return error_response(400, message)

@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response

@app.errorhandler(500)
def server_error(e):
    response = jsonify({'error': 'server error'})
    response.status_code = 500
    return response