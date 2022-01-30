import functools
from sqlite3 import IntegrityError

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.models import UserModel


bp = Blueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/auth',
)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if not error:
            try:
                UserModel.insert(username, generate_password_hash(password))
            except IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = UserModel.search_username(username)

        if not user:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if not error:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = UserModel.search_id(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
