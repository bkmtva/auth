from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.config import Config

app = Flask(__name__)
db = SQLAlchemy()

app.config.from_object(Config)

def create_app(config_class=Config):
    db.init_app(app)
    from application.routes import users
    app.register_blueprint(users)

    return app