from flask.ext.script import Manager

from gor0x import create_app
from gor0x.database import init_db, drop_db

manager = Manager(create_app)


@manager.command
def initdb():
    print 'Initialising database'
    init_db()
    print 'Database initialized'


@manager.command
def dropdb():
    print 'Dropping database'
    drop_db()
    print 'Database dropped'

