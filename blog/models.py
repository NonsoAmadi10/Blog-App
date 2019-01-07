from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from blog import db, login_manager, app
from flask_login import UserMixin

#loads user details when logged in 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20) , nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref= db.backref('author', lazy='joined'), lazy= 'select')


    
     #function to initialize reset passwords

    
    def reset_token(self):
        s = Serializer(app.config['SECRET_KEY'], 1800)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    #def __init__(self, username , email , password ):
        #self.reset_token = reset_token()
        #self.username = username
        #self.email = email
        #self.password = password
        


    @staticmethod
    def verify_token(token): #verifying token
         s = Serializer(app.config['SECRET_KEY'])

         try:
            user_id = s.loads(token)['user_id']
         except:
            return None
         return User.query.get(user_id)


    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}, {self.post}")'





class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable= False )
    date_posted = db.Column(db.DateTime, nullable=False , default= datetime.utcnow )
    content = db.Column(db.Text, nullable=False,)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"