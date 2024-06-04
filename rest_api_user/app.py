from functools import wraps
from flask import Flask, request, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
import os
#from dotenv import dotenv_values
from dotenv import load_dotenv

app = Flask(__name__)
# Replace with your own PostgreSQL database URI

loadedConfig = load_dotenv(override=False)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "postgresql://multichain:multichain@master:5432/multichain"
#dotenv_values: app.config['SQLALCHEMY_DATABASE_URI'] = loadedConfig['DATABASE_URL'] or "postgresql://multichain:multichain@localhost:5432/multichain"
global_token = os.environ.get('TOKEN') or "vattelapesca"
#dotenv_values: global_token = loadedConfig['TOKEN'] or "this-is-the-default-token"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'password': self.password}

    def __repr__(self):
        return f'<Item {self.name}>'

with app.app_context():
  db.create_all()

# Authentication decorator


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token or global_token != token:  # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
         # Return the user information attached to the token
        return f(*args, **kwargs)
    return decorator

# create


@app.route("/user", methods=["POST"])
@token_required
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# read - all


@app.route("/user", methods=['GET'])
@token_required
def get_all():
    try:
        users = User.query.all()
        return make_response(jsonify([user.to_dict() for user in users])), 200
    except Exception as e:
        return make_response(jsonify({'message': e}), 500)

# read - one


@app.route("/user/<int:id>", methods=["GET"])
@token_required
def get_one(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
        }), 200
    else:
        return jsonify({'status': 'fail', 'message': 'User not found'}), 404

# update


@app.route('/user/<int:id>', methods=['PUT'])
@token_required
def update_user(id):
    data = request.json
    user = User.query.get_or_404(id)
    user.name = data.get('username', user.username)
    user.password = data.get('password', user.password)
    db.session.commit()
    return jsonify(user.to_dict())

# delete


@app.route('/user/<int:id>', methods=['DELETE'])
@token_required
def delete_item(id):
    item = User.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

# confronta con i dati del db


@app.route("/user/checkCredential", methods=["POST"])
def check_credential():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        # query per verificare username e password su db
        user = User.query.filter_by(
            username=username, password=password).first()
        if user:
            return jsonify({'status': 'success', 'message': 'Login successful'}), 200
        else:
            return jsonify({'status': 'fail', 'message': 'Invalid username or password'}), 401
    except Exception as e:
        return make_response(jsonify({'message': e}))


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
