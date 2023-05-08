from flask import Flask, jsonify, request, current_app, abort
from functools import wraps
# from flask_jwt import JWT, jwt_required, current_identity
import jwt
from model import db, User
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'super-secret-key'
db.init_app(app)






@app.route('/auth/users/create', methods=['POST'])
def create():
    data = request.get_json()
    if 'name' not in data:
        return {'message': 'Username field cant be empty'}, 400
    if 'email' not in data:
        return {'message': 'Email field cant be empty'}, 400
    if 'password' not in data:
        return {'message': 'Write password'}, 400
    

    name = data['name']
    email = data['email']
    password = data['password']


    if User.query.filter_by(name=name).first():
        return {'message': 'Username already taken'}, 400
    if User.query.filter_by(email=email).first():
        return {'message': 'Email already taken'}, 400


    user = User(name=name, email=email)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user=User().get_by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["active"]:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated


def authenticate(email, password):
    
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user
    return False

@app.route('/auth/users/token', methods=['POST'])
def login():
    data = request.get_json()
    if 'email' not in data or "password" not in data:
        return jsonify({'message': 'Please provide credentials'}), 401
    
    email = data['email']
    password = data['password']

    user = authenticate(email, password)
    

    if user:
        print(user)
        access_token = jwt.encode({
            'username': user.id,
            'expiration': str(datetime.utcnow() + timedelta(minutes=30)),
            }, 
            app.config['SECRET_KEY'], algorithm="HS256"
            )
        print('access_token:', access_token)
        return jsonify({'access_token': access_token.decode('utf-8')})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
