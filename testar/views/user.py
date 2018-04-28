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
        return http_err(401, 'incorrect password')
    token = get_token(user.asdict())
    return http_ok(user.asdict(), jwt=token)


@app.route('/v1/register', methods=['POST'])
@make_json('username', 'email', 'password')
def user_register(data):
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    if new_user.email_exists():
        return http_err(404, 'user with given email already exists')
    if new_user.username_exists():
        return http_err(404, 'user with given username already exists')
    db.session.add(new_user)
    db.session.commit()
    token = get_token(new_user.asdict())

    # TODO: email verification

    return http_ok(new_user.asdict(), jwt=token)


@app.route('/v1/me', methods=['PATCH'])
@secured()
@make_json()
def me_patch(token_data, data):
    user = User.query.filter_by(id=token_data['id']).first()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if username:
        user.username

