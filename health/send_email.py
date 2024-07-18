from flask_mail import Message
from flask import render_template, current_app
from health import mail
from health.utils import generate_token

def send_password_reset_email(user):
    token = generate_token(user.email)
    msg = Message('Reset Your Password', sender='your-email@gmail.com', recipients=[user.email])
    msg.body = render_template('email/reset_password_request.txt', user=user, token=token)
    msg.html = render_template('email/reset_password.html', user=user, token=token)
    mail.send(msg)


