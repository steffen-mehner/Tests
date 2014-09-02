# -*- coding: utf-8 -*-
from enma.user.models import User, Role
from enma.database import db


def establish_all_roles_and_get_site_admin_role():
    Role.insert_roles()
    return Role.query.filter(Role.name=='SiteAdmin').first()


def establish_admin_defaults():
    """
    Reset the password of the admin user to admin.
    If the admin user does not exist he/she is created with minimal data.
    """
    admin = User.query.filter(User.username=='admin').first()
    if not admin:
        admin = User(username='admin', email='support@pixmeter.com',
                     password='admin', active=True)
    else:
        admin.set_password('admin')
    admin.role = establish_all_roles_and_get_site_admin_role() 
    db.session.add(admin)
    db.session.commit()
