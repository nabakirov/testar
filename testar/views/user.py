from testar import app
from testar.models import User
from flask import request
from testar.utils import http_err, http_ok, make_json
from testar import db
from testar.security import get_token, secured


@app.route('/v1/login', methods=['POST', 'GET'])
@make_json('testar', 'password')
def user_login(data):
    # TODO: email validation
    if '@' in data['testar']:
        user = User.query.filter_by(email=data['testar']).first()
    else:
        user = User.query.filter_by(username=data['testar']).first()
    if not user:
        return http_err(404, 'user with given credentials not found')
    if not user.verify_password(data['password']):
        return http_err(403, 'incorrect password')
    token = get_token(user.asdict())
    return http_ok(**user.asdict(), jwt=token)


@app.route('/v1/register', methods=['POST'])
@make_json('username', 'email', 'password')
def user_register(data):
    if User.query.filter_by(email=data['email']):
        return http_err(404, 'user with given email already exists')
    if User.query.filter_by(username=data['username']):
        return http_err(404, 'user with given username already exists')
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    token = get_token(new_user.asdict())

    # TODO: email verification

    return http_ok(**new_user.asdict(), jwt=token)


@app.route('/v1/me', methods=['PATCH'])
@secured()
@make_json()
def me_patch(token_data, data):
    for k, v in data.items():
        if k not in ['username', 'old_password', 'new_password', 'email']:
            return http_err(400, 'unknown parameter {}'.format(k))
    user = User.query.filter_by(id=token_data['id']).first()
    username = data.get('username')
    email = data.get('email')
    password = data.get('new_password')
    if username:
        if user.query.filter_by(username=username).first():
            return http_err(404, 'user with given username already exists')
        user.username = username
    if email:
        if user.query.filter_by(email=email).first():
            return http_err(404, 'user with given email already exists')
        user.email = email
    if password:
        old_password = data.get('old_password')
        if not old_password:
            return http_err(400, 'old password not given')
        if not user.verify_password(old_password):
            return http_err(401, 'old password did not match')
        user.password = password

    db.session.add(user)
    db.session.commit()
    return http_ok(**user.asdict())


