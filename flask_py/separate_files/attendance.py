from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from models import *
from errors import *

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password==password:
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token):
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

### ROUTES: ###

@app.route('/api/vessels')
@token_auth.login_required
def get_vessels():
    query = Vessel.query.order_by(Vessel.name)
    return jsonify({'data': [row.to_dict() for row in query],})

@app.route('/api/vessels/<int:id>')
@token_auth.login_required
def get_vessel(id):
    return_object = Vessel.query.get_or_404(id).to_dict()
    return jsonify({'data': [return_object],})

@app.route('/api/users')
@token_auth.login_required
def get_users():
    query = User.query
    return jsonify({'data': [row.to_dict() for row in query],})

@app.route('/api/users/<int:id>')
@token_auth.login_required
def get_user(id):
    return_object = User.query.get_or_404(id).to_dict()
    return jsonify({'data': [return_object],})

### Authentication: ###

@app.route('/api/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})