from flask import Blueprint , render_template, request
from blog.models import Post


Main = Blueprint('Main', __name__) 



@Main.route('/')
def home():
    page = request.args.get('page', 1 ,type=int) #Gets the type of page requested from the client and specifies nthe default number to 1 and if the client requests a page that is not an integer it throws an error
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page ,per_page=2) #accounts for the number of post per_page
    return render_template('home.html', title ="home" , posts= post)



@Main.route('/about')
def about():
    return render_template('about.html', title ="about" )



