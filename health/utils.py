from flask import current_app, abort, render_template, request, redirect, url_for, flash
from flask_mail import Message
from functools import wraps
from flask_login import current_user
import jwt
from datetime import datetime, timedelta
from health import mail

def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

def format_datetime(date):
    return date.strftime('%Y.%m.%d %H:%M:%S')

def get_current_timestamp():
    return datetime.utcnow()

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next=request.url))
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorated_view

def generate_token(email, expiration=None):
    if expiration is None:
        expiration = current_app.config['TOKEN_EXPIRATION']

    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(seconds=expiration)
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['email']
    except jwt.ExpiredSignatureError:
        return None  # Signature has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def data_analysis():
    return None

