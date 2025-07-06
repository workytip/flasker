import sqlite3
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
                )
        g.db.row_factory= sqlite3.Row

    return g.db


def close_db(e=None):
    # close the db conenecion when the app context is poped (deleted) (means, request is completed or errored)
    db = g.pop('db', None)
    
    # close the connection
    if db:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    '''Clear the existing data and create new tables'''
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
        'timestamp', lambda v: datetime.fromisoformat(v.decode())
        )

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def hello():
    print('hello world')
