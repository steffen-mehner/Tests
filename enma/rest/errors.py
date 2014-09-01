from flask import jsonify
from . import api


class ValidationError(ValueError):
    pass


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message='Invalid credentials'):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message='This request'):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response

def not_found(message='REST Object'):
    response = jsonify({'error': 'not_found', 'message': message})
    response.status_code = 404
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
