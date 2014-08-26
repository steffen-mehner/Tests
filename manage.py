#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import MigrateCommand

from enma.app import create_app
from enma.user.models import User
from enma.settings import DevConfig, ProdConfig
from enma.database import db
from enma.user.admin import establish_admin_defaults

if os.environ.get("ENMA_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)
TEST_CMD = "py.test tests"

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}

@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main(['tests', '--verbose'])
    return exit_code

@manager.command
def establish_admin():
    """
    Create the admin user or reset the admin to factory defaults
    I.e. the admin user password is set to 'admin' and the admin user
    has the role 'SiteAdmin'.
    """
    establish_admin_defaults()

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()