from flask import session, Blueprint, request, g, redirect, render_template, url_for
from werkzeug.exceptions import abort
from .auth import login_required 
from .db import get_db 

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' ORDER BY created DESC'
            ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        user_id = session['user_id']
        

        error = None
        db = get_db()

        if title is None:
            error = 'tilte is required'
        elif body is None:
            error = 'body is required'
        
        if error is not None:
            flash(error)
        else:
            db.execute('INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)', 
                       (user_id, title, body)
                       )
        db.commit()
        return redirect(url_for('index'))

        flash(error)
    return render_template('blog/create.html')

def get_post_by_id(id, check_author=True):
    db = get_db()
    
    post = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE p.id = ?', (id,)
            ).fetchone()
    
    if post is None:
        abort(404, f'Post id {id} doesn\'t exist')

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post_by_id(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        error = None
        db = get_db()

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db.execute(
                    'UPDATE post SET title = ?, body = ?'
                    ' WHERE id = ?',
                    (title, body, id)
                    )
            db.commit()
            return redirect(url_for('blog.index')) # blog.index is same as index we registered index at / in __init__.py
        
    
    return render_template('blog/update.html', post=post)

# delete post view
#   Require login
# 1- get the int:id from user
# 2- get_post_by_id
# 3- delete post 
# 4- commit
# 5- redirect to index
    
def delete_post_by_id(id):
    get_post_by_id(id)
    db = get_db()

    db.execute(
            'DELETE FROM post WHERE id = ?',
            (id,)
            )
    db.commit()


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    delete_post_by_id(id)
    
    return redirect(url_for('blog.index'))

