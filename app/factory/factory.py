from pathlib import Path

from flask import Flask

from app.commands import init_db_command
from app.database import Database
from app.views.auth import bp as auth
from app.views.blog import bp as blog


class AppFactory:
    def __init__(
        self,
        name: str,
        secret_key: str,
        database: str,
    ):
        self.name = name
        self.secret_key = secret_key
        self.database = database

    def init_app(
        self,
        app: Flask,
    ):
        app.teardown_appcontext(Database.close_db)
        app.cli.add_command(init_db_command)
        app.register_blueprint(auth)
        app.register_blueprint(blog)
        app.add_url_rule('/', endpoint='index')

    def create_app(
        self,
        test_config=None,
    ) -> Flask:
        app = Flask(
            self.name,
            instance_relative_config=True,
        )
        app.config.from_mapping(
            SECRET_KEY=self.secret_key,
            DATABASE=Path(app.instance_path, self.database)
        )

        if not test_config:
            app.config.from_pyfile('config.py', silent=True)
        else:
            app.config.from_mapping(test_config)

        Path.mkdir(Path(app.instance_path), parents=True, exist_ok=True)

        self.init_app(app)
        return app
