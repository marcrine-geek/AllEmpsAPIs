from threading import Thread

from flask import Flask
from flask_mail import Mail, Message

from config import DevelopmentConfig

# from app import app, mail

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
mail = Mail()
mail.init_app(app)


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except ConnectionRefusedError:
            return {"message": "Server not working"}


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()
    