from app.rest.api import cloud_manager
from functools import wraps
from flask import request, jsonify, abort


def expect(input, expectedType, field, *args):
    if input:
        if isinstance(input, expectedType):
            return input
        else:
            abort(400, 'Invalid input for {0}'.format(field))

    elif args:
        return args[0]

    return None


def required_body(fields):
    """
    Decorator to validate required parameters
    """

    def _file_content_validation_wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):

            data = request.get_json()
            for i in fields:
                if i not in data.keys():
                    return jsonify({'message': 'the key ``{0}`` is required'.format(i)}), 400
            return func(*args, **kwargs)

        return _wrapped

    return _file_content_validation_wrapper


def required_params(fields):
    """
    Decorator to validate required parameters
    """

    def _file_content_validation_wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):

            data = request.args
            for i in fields:
                if i not in data.keys():
                    return jsonify({'message': 'the key ``{0}`` is required'.format(i)}), 400
            return func(*args, **kwargs)

        return _wrapped

    return _file_content_validation_wrapper
