from datetime import datetime
from flask_mail import Message
from functools import wraps
from flask import abort, current_app
from flask_login import current_user

# Function for sending e-mails
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    with current_app.app_context():
        current_app.extensions['mail'].send(msg)

# Functions for working with dates
def format_datetime(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def get_current_timestamp():
    return datetime.utcnow()

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
