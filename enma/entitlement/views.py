# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, redirect, url_for
from flask.ext.login import login_required, current_user, logout_user

from enma.user.models import User
from enma.user.forms import DeleteForm, EditForm, ChangePasswordForm
from enma.database import db
from enma.utils import flash_errors

blueprint = Blueprint("entitlement", __name__, url_prefix='/entitlements',
                        static_folder="../static")


@blueprint.route("/")
@login_required
def list():
    return render_template("entitlements/list.html")

@blueprint.route("/requests")
@login_required
def requests():
    return render_template("entitlements/list.html")


@blueprint.route("/types")
@login_required
def types():
    return render_template("entitlements/types.html")
