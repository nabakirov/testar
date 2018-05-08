from testar import app, db
from testar.models import Group, Question, User
from testar.security import secured
from testar.utils import make_json, http_err, http_ok
from flask import request


def group_available(id, entry_group: Group):
    if entry_group.id == id:
        return False
    groups = Group.query.filter_by(group_id=entry_group.id).all()
    for group in groups:
        if not group_available(id, group):
            return False
    return True


@app.route('/v1/grouping', methods=['POST', 'DELETE'])
@secured('admin manager')
@make_json()
def grouping(data, token_data):
    if data.get('group'):
        if not isinstance(data['group'], int):
            return http_err(400, 'group must be int, question id')
    else:
        return http_err(400, 'group parameter is missing')
    group = Group.query.filter_by(id=data['group'], user_id=token_data['id']).first()
    if not group:
        return http_err(404, 'group not found')
    if data.get('questions'):
        if not isinstance(data['questions'], (int, list)):
            return http_err(400, 'question must be int or array, question id')
        if isinstance(data['questions'], int):
            data['questions'] = [data['questions']]
        resp = []

        for q_id in data['questions']:
            question = Question.query.filter_by(id=q_id, user_id=token_data['id'])
            if not question:
                return http_err(404, 'question not found')
            if request.method == 'POST':
                question.group_id = group.id
            else:
                question.group_id = None
            db.session.add(question)
            resp.append(question.asdict())


        db.session.commit()
        return http_ok(group=group.asdict(), question=resp)

    if data.get('entry_group'):
        if not isinstance(data['entry_group'], (int, list)):
            return http_err(400, 'entry_group must be int or array')
        if isinstance(data['entry_group'], int):
            data['entry_group'] = [data['entry_group']]
        resp = []
        for g_id in data['entry_group']:
            entry_group = Group.query.filter_by(id=g_id, user_id=token_data['id']).first()
            if not entry_group:
                return http_err(404, 'entry_group not found')
            if not group_available(group.id, entry_group):
                return http_err(400, 'recursion error')
            if request.method == 'POST':
                entry_group.group_id = group.id
            else:
                entry_group.group_id = None

            db.session.add(entry_group)
            resp.append(entry_group.asdict())
        db.session.commit()
        return http_ok(group=group.asdict(), entry_group=resp)


@app.route('/v1/groups', methods=['POST'])
@secured('admin manager')
@make_json('title')
def groups_post(data, token_data):
    if data.get('description'):
        if not isinstance(data['description'], str):
            return http_err(400, 'description parameter must be string')

        group = Group(title=data['title'], description=data['description'], user_id=token_data['id'])
    else:
        group = Group(title=data['title'], user_id=token_data['id'])
    db.session.add(group)
    db.session.commit()
    if data.get('questions'):
        unknowns = []
        if not isinstance(data['questions'], list):
            return http_err(400, 'questions parameter must be array')
        for q_id in data['questions']:
            question = Question.query.get(q_id)
            if not question:
                unknowns.append(q_id)
                continue
            question.group_id = group
            db.session.add(question)
        db.session.commit()
    return http_ok(**group.asdict())


@app.route('/v1/groups')
@secured('manager admin')
def groups_get(token_data):
    user = User.query.get(token_data['id'])
    groups = [g.asdict() for g in user.groups]
    return http_ok(groups=groups)


def get_group_tree(group: Group):
    groups = Group.query.filter_by(group_id=group.id).all()
    questions = Question.query.filter_by(group_id=group.id)
    g_dict = group.asdict()
    g_dict['questions'] = [q.asdict() for q in questions]
    g_dict['groups'] = [get_group_tree(g) for g in groups]
    return g_dict


@app.route('/v1/groups/<id>')
@secured('manager admin')
def group_get(token_data, id):
    group = Group.query.filter_by(id=id, user_id=token_data['id']).first()
    if not group:
        return http_err(404, 'group not found')
    return http_ok(**get_group_tree(group))
