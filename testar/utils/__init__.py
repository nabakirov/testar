from flask import jsonify, request
import functools as FT


def http_ok(data: dict, message='ok', code=200, **kwargs):
    if not isinstance(data, dict):
        raise TypeError('data must be dict')
    data.update(dict(message=message, code=code))
    data.update(kwargs)
    return jsonify(data), code


def http_err(code, message, **kwargs):
    data = dict(code=code, message=message)
    data.update(kwargs)
    return jsonify(data), code


def make_json(*args, **kwargs):
    keys = args

    def wrapper_of_wrapper(f):

        @FT.wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json(force=True, silent=True)
            if not data:
                return http_err(400, 'json required')
            for r in keys:
                if r not in data:
                    return http_err(400, '{} is missing'.format(r))

            return f(*args, **kwargs, **dict(data=data))

        return wrapper
    return wrapper_of_wrapper