# -*- coding: utf-8 -*-
#
# Copyright (c) 2014  Ingenieurbüro Volker Kempert
#
"""
@file
Example of a Rest API (not authorized access)

Copied from:
http://blog.miguelgrinberg.com/post/restful-authentication-with-flask
"""
import logging

from flask import jsonify, abort, request, render_template, Blueprint


rest = Blueprint("rest-entitlement", __name__,
                 url_prefix='/rest/v1.0')


logger = logging.getLogger(__name__)
logger.info('module imported')

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


@rest.route('/entitlements', methods=['GET'])
def get_entitlements():
    """
    Respond with the list of all entitlements
    """
    logger.info('get_entitlements called')
    return jsonify({'entitlements': entitlements})


@rest.route('/entitlements/<name>', methods=['GET'])
def get_entitlement(name):
    """
    Respond with the granted i.e. valid entitlement by name or with
    404 - Not found 
    """
    logger.info('get_entitlement %s called', name)
    tmp = filter(lambda x: x['name'] == name and x['status'] == 'granted',
                 entitlements)
    if len(tmp) == 0:
        return not_found()
    return jsonify({'entitlements': tmp[0]})


@rest.route('/users/token', methods=['GET'])
def get_rest_token():
    """
    Get the current Authentication token
    """
    return jsonify({'token': 'abcdefg-token', 'expiry': '20140901'})

@rest.route('/users/token', methods=['PUT'])
def create_new_rest_token():
    """
    Create new Authentication token and return it
    """
    return jsonify({'token': 'abcdefg-new-token', 'expiry': '20140901'}), 201


def unauthorized(message):
    """ 
    Helper function to handle missing authentication data failure
    """
    response = jsonify({'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    return response



def forbidden(message):
    """ 
    Helper function to handle authentication failures and lack of permission
    """
    response = jsonify({'error': 'forbidden',
                        'message': message})
    response.status_code = 403
    return response


def not_found():
    """ 
    Helper function to indicating a resource was not found
    """
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response



