from application import db
from datetime import datetime, timedelta
from application import create_app
from flask_restful import Api
from application.routes import authentication_routes
from flask_jwt_extended import JWTManager
app = create_app()

jwt = JWTManager(app)
api = Api(app)
authentication_routes(api)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
