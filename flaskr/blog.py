from flask import(
        Blueprint, flash, g, redirect, render_template,request, url_for
        )
from werkzeug.exceptions import abort
from sqlalchemy import desc

from flaskr.auth import login_required
from flaskr import db
from flaskr.models import User, Post

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = User.query.join(Post, User.user_id == Post.author_id).order_by(desc(Post.created))
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user['user_id'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
        
    return render_template('blog/create.html')

def get_post(id, check_author = True):
    post = Post.query.join(User, Post.author_id == User.user_id).filter_by(id=id).one()
    
    if post is None:
        abort(404, "Post id {0} doesn't exist".format(id))
    
    if check_author and post.author_id != g.user['user_id']:
        abort(403)
    
    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
