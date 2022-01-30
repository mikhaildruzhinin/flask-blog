from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from .auth import login_required
from .models import PostModel


bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    posts = PostModel.get_all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required'

        if error:
            flash(error)
        else:
            PostModel.create(title, body, g.user['id'])
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


def get_post(post_id, check_author=True):
    post = PostModel.search_post_id(post_id)
    if not post:
        abort(404, f'Post id {post_id} doesn\'t exist')
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = get_post(post_id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
    
        if not title:
            error = 'Title is required.'

        if error:
            flash(error)
        else:
            PostModel.update(title, body, post_id)
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    get_post(post_id)
    PostModel.delete(post_id)
    return redirect(url_for('blog.index'))
