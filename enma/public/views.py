# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session)
from flask.ext.login import login_user, login_required, logout_user

from enma.extensions import login_manager
from enma.user.models import User
from enma.public.forms import LoginForm
from enma.user.forms import RegisterForm
from enma.utils import flash_errors
from enma.database import db

blueprint = Blueprint('public', __name__, static_folder="../static")

@login_manager.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data,
                        active=True)
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/help/")
def help():
    form = LoginForm(request.form)
    return render_template("public/help.html", form=form)


@blueprint.route("/about/")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route("/contact/")
def contact():
    form = LoginForm(request.form)
    return render_template("public/contact.html", form=form)


@blueprint.route("/legal/")
def legal():
    form = LoginForm(request.form)
    return render_template("public/legal.html", form=form)


@blueprint.route("/privacy/")
def privacy():
    form = LoginForm(request.form)
    return render_template("public/privacy.html", form=form)

@blueprint.route("/terms/")
def terms():
    form = LoginForm(request.form)
    return render_template("public/terms.html", form=form)