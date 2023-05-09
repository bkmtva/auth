from flask import request
from application import db
from application.model import User
from functools import wraps
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from application.email import send_email
from application.token import confirm_token


class Create(Resource):
    def post(self):
        
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
        
        subject = "Please confirm your email"

        send_email(email, subject, email)

        user = User(name=name, email=email, confirmed=False)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()

        
        return f'Email you entered {email}'
    

class Verify(Resource):
    def get(self, token):
        try:
            
            email = confirm_token(token)
            if not email:
                User.query.filter(User.confirmed == False).delete()
                db.session.commit()
                return {'message': 'Your token is expired or wrong email, please try again'}, 200
        except:
            User.query.filter(User.confirmed == False).delete()
            db.session.commit()
            return {'message': 'Your token is expired or wrong email, please try again'}, 200
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            return {'message': 'Account already confirmed. Please login.'}, 200
        else:
            user.confirmed = True
            # user.confirmed_on = datetime.now()
            db.session.add(user)
            db.session.commit()
            return 'You have confirmed your account!', 200

    # def get(self, token='token'):
    #     return 'Verification message sended to your email', 200
def authenticate(email, password):
    
    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        return user
    return False

class Token(Resource):
    def post(self):
        data = request.get_json()
        if 'email' not in data or "password" not in data:
            return {'message': 'Please provide credentials'}, 401
        
        email = data['email']
        password = data['password']

        user = authenticate(email, password)

        if user:
            expires = timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401





    

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if "Authorization" in request.headers:
#             token = request.headers["Authorization"].split(" ")[1]
#         if not token:
#             return {
#                 "message": "Authentication Token is missing!",
#                 "data": None,
#                 "error": "Unauthorized"
#             }, 401
#         try:
#             data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
#             current_user=User().get_by_id(data["user_id"])
#             if current_user is None:
#                 return {
#                 "message": "Invalid Authentication token!",
#                 "data": None,
#                 "error": "Unauthorized"
#             }, 401
#             if not current_user["active"]:
#                 abort(403)
#         except Exception as e:
#             return {
#                 "message": "Something went wrong",
#                 "data": None,
#                 "error": str(e)
#             }, 500

#         return f(current_user, *args, **kwargs)

#     return decorated

