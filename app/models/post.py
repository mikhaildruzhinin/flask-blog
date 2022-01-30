from app.database import Database
from app.models.user import UserModel


class PostModel:
    __tablename__ = 'post'

    @classmethod
    def get_all(cls):
        db = Database.get_db()

        select_query = \
            '''select p.id, p.title, p.body, p.created, p.author_id, u.username
            from {} p join {} u on p.author_id = u.id
            order by created desc'''.format(
                cls.__tablename__,
                UserModel.__tablename__,
            )
        return db.execute(select_query).fetchall()

    @classmethod
    def create(
        cls,
        title: str,
        body: str,
        author_id: int,
    ):
        db = Database.get_db()

        insert_query = \
            '''insert into {} (title, body, author_id)
            values (?, ?, ?)'''.format(
                cls.__tablename__
            )

        db.execute(
            insert_query,
            (title, body, author_id)
        )
        db.commit()

    @classmethod
    def search_post_id(
        cls,
        post_id: int,
    ):
        db = Database.get_db()

        select_query = \
            '''select p.id, title, body, created, author_id, username
            from {} p join {} u on p.author_id = u.id
            where p.id = ?'''.format(
                cls.__tablename__,
                UserModel.__tablename__,
            )
        return db.execute(select_query, (post_id,)).fetchone()

    @classmethod
    def update(
        cls,
        title: str,
        body: str,
        post_id: int,
    ):
        db = Database.get_db()

        update_query = \
            '''update {} set title = ?, body = ?
            where id = ?'''.format(
                cls.__tablename__
            )

        db.execute(update_query, (title, body, post_id))
        db.commit()

    @classmethod
    def delete(
        cls,
        post_id: int,
    ):
        db = Database.get_db()

        update_query = \
            'delete from {} where id = ?'.format(
                cls.__tablename__
            )

        db.execute(update_query, (post_id,))
        db.commit()
