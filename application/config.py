import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SECRET_KEY = 'super-secret-key'
    # SECURITY_PASSWORD_SALT = 'my_precious_two'
    SECURITY_PASSWORD_SALT = 'email-confirm'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    # MAIL_USERNAME = os.environ.get('EMAIL')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    MAIL_USERNAME = os.environ['EMAIL']
    MAIL_PASSWORD = os.environ['PASSWORD']
    

    # mail accounts
    MAIL_DEFAULT_SENDER = 'diana@gmail.com'


