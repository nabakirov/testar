from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from config import Config
import functools as FT
from flask import request
from testar.utils import http_err
from inspect import signature


def get_token(data: dict, exp=Config.TOKEN_EXP):
    s = Serializer(Config.SECRET_KEY, exp)
    if not isinstance(data, dict):
        raise TypeError('data must be dict')
    return s.dumps(data).decode()


def secured():
    def wrapper_of_wrapper(f):
        params = signature(f).parameters
        secured_keys = {'token_data', 'token'}.intersection(params.keys())

        @FT.wraps(f)
        def wrapper(*args, **kwargs):
            authorization = request.headers.get('Authorization')
            if not authorization:
                return http_err(401, 'authorization required')
            if authorization.startswith('Bearer '):
                token = authorization[7:]
            else:
                token = authorization
            s = Serializer(Config.SECRET_KEY)
            try:
                token_data = s.loads(token.encode())
            except (BadSignature, SignatureExpired):
                return False
            secured_kwargs = dict(token_data=token_data, token=token)
            secured_kwargs = {
                k: v
                for k, v in secured_kwargs.items() if k in secured_keys
            }
            return f(*args, **kwargs, **secured_kwargs)
        return wrapper
    return wrapper_of_wrapper


