# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest
from flask import url_for


from enma.user.models import User, Role
from enma.database import db
from .factories import UserFactory
from enma.user.admin import establish_admin_defaults
from enma.user.admin import establish_and_get_site_admin_role


class TestLoggingIn:

    def test_can_log_in_returns_200(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res


class TestRegistering:

    def test_can_register(self, user, testapp):
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get("/")
        # Clicks Create Account button
        res = res.click("Create account")
        # Fills out the form
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but passwords don't match
        form = res.forms["registerForm"]
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert "Passwords must match" in res

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but username is already registered
        form = res.forms["registerForm"]
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert "Username already registered" in res


def does_user_have_role(user, role_name):
        found = False
        for role in user.roles:
            if role.name == role_name:
                found = True
        return found

class TestEstablishAdminDefaults:

    def test_create_if_not_exists(self, user, testapp):
        admin = User.query.filter(User.username=='admin').first()
        if admin:
            db.session.delete(admin)
            db.session.commit()
        # no admin user exists anymore

        establish_admin_defaults()
        admin = User.query.filter(User.username=='admin').first()
        assert admin # admin user exists
        assert admin.check_password('admin') # has the password admin

    def test_reset_passwd_if_exists(self, user, testapp):
        admin = User.query.filter(User.username=='admin').first()
        if admin:
            admin.set_password('not-admin')
        else:
            admin = User('admin', 'foo@test.com', password='not-admin')
        db.session.add(admin)
        db.session.commit()

        establish_admin_defaults()
        admin = User.query.filter(User.username=='admin').first()
        assert admin # admin user exists
        assert admin.check_password('admin') # has the password admin

    def test_set_site_admin_role(self, user, testapp):
        admin = User.query.filter(User.username=='admin').first()
        if not admin:
            admin = User('admin', 'foo@test.com')
        db.session.add(admin)
        db.session.commit()

        establish_admin_defaults()
        retrieved = User.query.filter(User.username=='admin').first()
        assert retrieved 
        assert does_user_have_role(retrieved, 'SiteAdmin')

    def test_site_admin_role_exists(self, user, testapp):
        site_admin_role = establish_and_get_site_admin_role()
        roles = Role.query.all()
        found = False
        for role in roles:
            if role.name == 'SiteAdmin':
                found = True
                assert role == site_admin_role
        assert found
