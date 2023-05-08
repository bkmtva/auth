from flask_restful import Api
from users.views import LoginApi, ForgotPassword, SignUpApi, ResetPassword


def authentication_routes(api: Api):
    api.add_resource(SignUpApi, "/api/auth/create/")
    api.add_resource(LoginApi, "/api/auth/token/")
    