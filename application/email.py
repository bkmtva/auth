from flask_mail import Message
from application import app
from flask_mail import Mail
from flask import url_for
from application.token import generate_confirmation_token
mail = Mail(app)
def send_email(to, subject, email):
    msg = Message(
        subject,
        recipients=[to],
        sender=app.config["MAIL_DEFAULT_SENDER"],
       
        
    )
    token = generate_confirmation_token(email)
    link = url_for('verify', token=token, _external=True)
    msg.body = f'Verification link {link}'
    
    print(msg)
    mail.send(msg)
    