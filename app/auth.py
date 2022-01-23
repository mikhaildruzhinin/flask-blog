import functools

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

from app.database import Database


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
        db = Database.get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        
        if error:
            try:
                db.execute(
                    'insert into user (username, password) values (?, ?)',
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')


bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = Database.get_db()
        error = None
        
        user = db.execute(
            'select id, username, password from user where username = ?',
            (username,)
        ).fetchone()

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


@bp.before_app_first_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if not user_id:
        g.user = None
    else:
        g.user = Database.get_db().execute(
            'select id, username, password from user where id = ?',
            (user_id,)
        ).fetchone()


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
