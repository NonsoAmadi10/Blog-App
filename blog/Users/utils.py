import os
import secrets
from flask import  url_for
from blog  import app, mail
from PIL import Image
from flask_mail import Message






def save_picture(form_picture): #initializes profile picture save
    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn) #specifies the path which the images should be saved
    output_size = (125, 155)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.reset_token()
    msg = Message('Password Reset', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f''' We heard you lost your password. Please kindly follow this link with instructions to how reset your password:
{url_for('users.reset_token',token=token, _external=True)}

If you did not make this request, kindly ignore this message and no changes will be made   
'''


