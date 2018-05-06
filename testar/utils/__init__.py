from flask import jsonify, request
import functools as FT
import random
from copy import deepcopy


def http_ok(message='ok', code=200, **kwargs):
    data = dict(code=code, message=message)
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


def mix(arr: list):
    length = len(arr)
    mixed = [None] * length
    buffer = deepcopy(arr)
    c = length - 1
    for i, obj in enumerate(arr):
        ri = random.randint(0, c)
        mixed[i] = buffer[ri]
        del(buffer[ri])
        c -= 1
    return mixed

