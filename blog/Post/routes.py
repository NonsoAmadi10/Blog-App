from flask import (Blueprint , render_template ,flash , redirect, request,
url_for,abort )

from blog import db
from flask_login import current_user , login_required
from blog.models import Post
from blog.Post.forms import NewPostForm


Posts = Blueprint('post', __name__)


@Posts.route('/post/new', methods= ["GET","POST"])
def new_post():
    form= NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('New Post Added','success')
        return redirect(url_for('Main.home'))
               

    return render_template('New.html', title='New Post', form=form, legend='New Post')




@Posts.route('/post/<int:post_id>')
def post(post_id):
    post= Post.query.get_or_404(post_id)

    return render_template('post.html', title=post.title,post=post)





@Posts.route('/post/<int:post_id>/edit', methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPostForm()
    
    if  request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    else:
        if form.validate_on_submit:
            post.title = form.title.data
        post.content= form.content.data
        db.session.commit()
        flash('Post Successfully Updated', 'success')
        return redirect(url_for('post.post',post_id=post.id))

    return render_template('New.html', title='Edit Post', form=form ,legend='Edit Post')
    


@Posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post successfully deleted!','success')
    return redirect(url_for('Main.home'))








    




