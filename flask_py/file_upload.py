from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
import base64

app = Flask(__name__)

# https://stackoverflow.com/questions/18208492/sqlalchemy-exc-operationalerror-operationalerror-unable-to-open-database-file
# Valid SQLite URL forms are:
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/agou/Desktop/src_tests/flask_test/db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'new_employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    photo = db.Column(db.BLOB) # https://stackoverflow.com/questions/29251431/python-flask-blob-image-sqlite-sqlalchemy-display-image
    resume = db.Column(db.BLOB)

    def to_dict(self):
      if self.photo:
        return {
            'id': self.id,
            'name': self.name,
            'photo': base64.b64encode(self.photo).decode("ascii")
        }
      else:
        return {
            'id': self.id,
            'name': self.name,
        }
    
    def from_dict(self, data):
        for field in ['id', 'name']:
            if field in data:
                setattr(self, field, data[field])
        for field in ['photo', 'resume']:
            if field in data:
                setattr(self, field, bytes(data[field], 'ascii'))

@app.route('/employees')
def get_employees():
    query = Employee.query
    return jsonify({
        'data': [user.to_dict() for user in query],
    })

@app.route('/employees/<int:id>')
def get_employee(id):
    employee = Employee.query.get_or_404(id).to_dict()
    return jsonify({
        'data': [employee],
    })

@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json() or {}
    new_employee = Employee()
    new_employee.from_dict(data)
    db.session.add(new_employee)
    db.session.commit()
    response = jsonify(new_employee.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_employee', id=new_employee.id)
    return response