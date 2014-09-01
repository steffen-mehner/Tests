# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import g, jsonify

from enma.extensions import auth
from . import api
from .errors import not_found


@api.route("/token", methods=["PUT"])
@auth.login_required
def token():
    return jsonify({
        'token': g.current_user.generate_auth_token(expiration=3600),
        'expiration': 3600}), 201


entitlements = [
    {
        'name': u'service-one',
        'type': u'service-one',
        'status': u'granted',
        'description': u'Use service one',
        'expiry': u'2014-09-20'
    },
    {
        'name': u'service-two',
        'type': u'service-two',
        'status': u'rewoked',
        'description': u'Use service two',
        'capacity': 500,
        'expiry': u'2014-09-20'
    },
]


@api.route('/entitlements', methods=['GET'])
@auth.login_required
def get_entitlements():
    """
    Respond with the list of all entitlements
    """
    return jsonify({'entitlements': entitlements})


@api.route('/entitlements/<name>', methods=['GET'])
@auth.login_required
def get_entitlement(name):
    """
    Respond with the granted i.e. valid entitlement by name or with
    404 - Not found 
    """
    tmp = filter(lambda x: x['name'] == name and x['status'] == 'granted',
                 entitlements)
    if len(tmp) == 0:
        return not_found('entitlement named %s' % name)
    return jsonify({'entitlements': tmp[0]})


