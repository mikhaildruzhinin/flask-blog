from pathlib import Path

from flask import Flask


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

    return app
