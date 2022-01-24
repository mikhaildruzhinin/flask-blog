from werkzeug.security import generate_password_hash

from app.database import Database


class UserModel:
    __tablename__ = 'user'

    @classmethod
    def insert(
        cls,
        username: str,
        password: str,
    ):
        db = Database.get_db()

        insert_query = \
            'insert into {} (username, password) values (?, ?)'.format(
                cls.__tablename__
            )

        db.execute(
            insert_query,
            (username, generate_password_hash(password))
        )

    @classmethod
    def search_username(
        cls,
        username: str,
    ):
        db = Database.get_db()

        select_query = \
            'select id, username, password from {} where username = ?'.format(
                cls.__tablename__
            )

        return db.execute(
            select_query,
            (username,)
        ).fetchone()

    @classmethod
    def search_id(
        cls,
        _id: int,
    ):
        db = Database.get_db()

        select_query = \
            'select id, username, password from {} where id = ?'.format(
                cls.__tablename__
            )

        return db.execute(
            select_query,
            (_id,)
        ).fetchone()
