# -*- coding: utf-8 -*-
from enma.user.models import User, Role
from enma.database import db


def establish_and_get_site_admin_role():
    site_admin_role = Role.query.filter(Role.name=='SiteAdmin').first()
    if not site_admin_role:
        site_admin_role = Role('SiteAdmin')
        db.session.add(site_admin_role)
        db.session.commit()
    return site_admin_role


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
    site_admin_role = establish_and_get_site_admin_role()
    #if site_admin_role in admin.roles:
    admin.roles.append(site_admin_role) 
    db.session.add(admin)
    db.session.commit()
