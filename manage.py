#!/usr/bin/env python
from app import app, db
from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
