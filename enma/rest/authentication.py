from flask import g
from flask.ext.login import AnonymousUserMixin as AnonymousUser

from enma.extensions import auth
from enma.user.models import User

from . import api
from .errors import unauthorized, forbidden, not_found


@auth.verify_password
def verify_password(username_or_token, password):
    if username_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(username_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=username_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.check_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route("/<path:invalid_path>")
def missing_resource(invalid_path):
    return not_found('invalid_path')