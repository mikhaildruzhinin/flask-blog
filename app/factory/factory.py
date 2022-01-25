from pathlib import Path

from flask import Flask

from .. import auth
from app.database import Database
from app.commands import init_db_command


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
        app.register_blueprint(auth.bp)

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

        @app.route('/')
        def hello():
            return 'Hello world!'

        self.init_app(app)
        return app
