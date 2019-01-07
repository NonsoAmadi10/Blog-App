import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



app = Flask(__name__)
app.config['SECRET_KEY'] ='3b3c2b95efa44c0d7bb47821bc54804c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///point.db'
app.static_folder = 'static'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message = "Please log in"
login_manager.login_message_category = "info"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nonnypyg@gmail.com'
app.config['MAIL_PASSWORD'] = 'chinonso'
mail = Mail(app)




from blog.Users.routes import users
from blog.Main.routes import Main
from blog.Post.routes import Posts

app.register_blueprint(users)
app.register_blueprint(Main)
app.register_blueprint(Posts)

