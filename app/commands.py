import click
from flask.cli import with_appcontext

from .database import Database


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables """
    Database.init_db()
    click.echo('Initialized the database')
