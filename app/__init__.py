from pathlib import Path

from flask import Flask

from . import auth
from .database import Database
from .commands import init_db_command


def init_app(app: Flask):
    app.teardown_appcontext(Database.close_db)
    app.cli.add_command(init_db_command)
    app.register_blueprint(auth.bp)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=Path(app.instance_path, 'db.sqlite')
    )

    if not test_config:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    Path.mkdir(Path(app.instance_path), parents=True, exist_ok=True)

    @app.route('/')
    def hello():
        return 'Hello world!'

    init_app(app)
    return app
