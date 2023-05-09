from flask_restful import Api
from application.views import Create, Token, Verify
from flask import Blueprint

users = Blueprint("users", __name__)

def authentication_routes(api: Api):
    api.add_resource(Create, "/auth/users/create")
    api.add_resource(Token, "/auth/users/token")
    api.add_resource(Verify, "/auth/users/verify/<token>")
    