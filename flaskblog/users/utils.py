from flask import url_for, current_app
import secrets
import os
from PIL import Image
from flask_mail import Message
from flaskblog import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics/' + picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_secret_token()
    msg = Message('Reset Password Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password follow the below link: 
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no change will happen.
'''
    mail.send(msg)
