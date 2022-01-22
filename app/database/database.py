import sqlite3

from flask import (
    current_app,
    g,
)


class Database:
    @staticmethod
    def get_db():
        if 'db' not in g:
            g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
        return g.db

    @staticmethod
    def close_db(_):
        db = g.pop('db', None)

        if db:
            db.close()

    @classmethod
    def init_db(cls):
        db = cls.get_db()

        with current_app.open_resource('database/schema/baseline.sql') as f:
            db.executescript(f.read().decode('utf-8'))
