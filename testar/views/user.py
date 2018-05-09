from testar import app
from testar.models import User, Competition, Submission, Test
from flask import request
from testar.utils import http_err, http_ok, make_json
from testar import db
from testar.security import get_token, secured
from time import time as now


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
@make_json('username', 'email', 'password', 'first_name', 'last_name')
def user_register(data):
    if User.query.filter_by(email=data['email']).first():
        return http_err(404, 'user with given email already exists')
    if User.query.filter_by(username=data['username']).first():
        return http_err(404, 'user with given username already exists')
    if not isinstance(data['first_name'], str):
        return http_err(400, 'first name must be string')
    if not isinstance(data['last_name'], str):
        return http_err(400, 'last_name must be string')
    new_user = User(username=data['username'], email=data['email'], password=data['password'],
                    first_name=data['first_name'], last_name=data['last_name'])
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


@app.route('/v1/me/competitions')
@secured()
def me_competitions(token_data):
    user = User.query.get(token_data['id'])
    return http_ok(competitions=[c.asdict() for c in user.competitions])


@app.route('/v1/me/competitions/<id>')
@secured()
def me_competition_submission(token_data, id):
    user = User.query.get(token_data['id'])
    competition = Competition.query.get(id)
    if not competition:
        return http_err(404, 'competition not found')
    if now() < competition.end_date:
        return http_err(404, 'competition not finished yet')
    if not competition:
        return http_err(404, 'competition not found')
    submissions = Submission.query.filter_by(user_id=user.id, competition_id=competition.id).all()
    if not submissions:
        return http_err(404, 'you have not submitted yet')

    test = Test.query.get(competition.test_id)
    questions = test.questions
    q_dict = []
    for question in questions:
        answers = [a.asdict() for a in question.answers]
        question = question.asdict()
        question['answers'] = answers
        q_dict.append(question)
    test = test.asdict()
    test['questions'] = q_dict
    return http_ok(test=test, submission=[s.asdict() for s in submissions])


@app.route('/v1/users')
@secured('admin manager')
def users_get():
    users = User.query.filter_by(admin=False, manager=False).all()
    users = [user.asdict() for user in users]
    return http_ok(users=users)