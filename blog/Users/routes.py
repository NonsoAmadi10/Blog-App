from flask import Blueprint ,render_template, url_for, flash, redirect,request, abort
from flask_login import login_user, current_user, logout_user, login_required
from blog  import app, bcrypt, db
from blog.models  import User, Post
from blog.Users.forms import RegistrationForm, LoginForm,UpdateAccountForm, RequestResetForm, ResetPasswordForm
from blog.Users.utils import save_picture, send_reset_email
users = Blueprint('users',__name__)



@users.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form  = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        #db.session.rollback()
        db.session.commit()
        flash('Account was successfully created! You can now log in', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html',title='registration form' , form = form)




@users.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome {current_user.username} ','success')
            
            return redirect(next_page) if next_page else redirect(url_for('Main.home'))
            

        else:
            flash(f'Log in unsuccesful, try again', "danger" )
    return render_template('login.html',title='Login |' ,form = form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('Main.home'))




@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) #saves the updated picture
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data 
        db.session.commit()
        flash('Account Successfully Updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pic/'+ current_user.image_file)
   
    
    return render_template('account.html', title='Account' ,image_file=image_file, form=form)



@users.route('/user/<string:username>')
def user_post(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1 ,type=int) #Gets the type of page requested from the client and specifies nthe default number to 1 and if the client requests a page that is not an integer it throws an error
    post = Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page ,per_page=2) #accounts for the number of post per_page
    return render_template('user_post.html', title ="User Post" , posts= post, username=user)




@users.route('/reset_Password/', methods= ["GET","POST"])
def pwd_reset():    
    
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    form= RequestResetForm()
    if request.method == "GET":
            return render_template('RequestPassword.html' , title='Request Password Reset', form=form)
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions on how to reset your password ', 'info')
        return redirect(url_for('users.login'))
    



@users.route('/reset_Password/<token>', methods= ["GET","POST"])
def reset_token(token):    
    if current_user.is_authenticated:
        return redirect(url_for('Main.home'))
    user = User.verify_token(token)
    if user is None:
        flash('This is an invalid or expired  token', 'warning')
        return redirect(url_for('users.pwd_reset'))
    form= ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        
        db.session.commit()
        flash('Password has been updated successfully! You can now log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset.html', title='Reset Password', form=form)
    




