from testar import app, db
from testar.models import Group, Question, User, GroupsGroups
from testar.security import secured
from testar.utils import make_json, http_err, http_ok
from flask import request


def group_available(id: int, entry: int):
    if id == entry:
        return False
    groups = GroupsGroups.query.filter_by(group=entry).all()
    for group in groups:
        if not group_available(id, group.entry):
            return False
    return True


@app.route('/v1/grouping', methods=['POST', 'DELETE'])
@secured('admin manager')
@make_json()
def grouping(data, token_data):
    if data.get('group'):
        if not isinstance(data['group'], int):
            return http_err(400, 'group must be int')
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
            question = Question.query.filter_by(id=q_id, user_id=token_data['id']).first()
            if not question:
                return http_err(404, 'question {} not found'.format(q_id))
            if request.method == 'POST':
                if question not in group.questions:
                    group.questions.append(question)
            else:
                if question in group.questions:
                    group.questions.remove(question)
            db.session.add(group)
            resp.append(question.asdict())


        db.session.commit()
        return http_ok(**group.asdict(), question=resp)

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
            if not group_available(group.id, entry_group.id):
                return http_err(400, 'recursion error')
            group_group = GroupsGroups.query.filter_by(group=group.id, entry=entry_group.id).first()
            if request.method == 'POST':
                if not group_group:
                    group_group = GroupsGroups(group=group.id, entry=entry_group.id)
                    db.session.add(group_group)
            else:
                if group_group:
                    db.session.delete(group_group)

            resp.append(entry_group.asdict())
        db.session.commit()
        return http_ok(**group.asdict(), entry_group=resp)
    return http_err(400, 'questions or entry_group parameter is missing')


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
    unknowns = []
    if data.get('questions'):
        if not isinstance(data['questions'], list):
            return http_err(400, 'questions parameter must be array')
        for q_id in data['questions']:
            question = Question.query.get(q_id)
            if not question:
                unknowns.append(q_id)
                continue
            group.questions.append(question)
    if data.get('users'):
        if not isinstance(data['users'], list):
            return http_err(400, 'users parameter must be array')
        for u_id in data['users']:
            user = User.query.get(u_id)
            if not user:
                unknowns.append(u_id)
                continue
            group.users.append(user)
    db.session.add(group)
    db.session.commit()
    return http_ok(**group.asdict())


@app.route('/v1/groups')
@secured('manager admin')
def groups_get(token_data):
    groups = Group.query.filter_by(user_id=token_data['id']).all()
    groups = [g.asdict() for g in groups]
    return http_ok(groups=groups)


def get_group_tree(group):
    group_ids = GroupsGroups.query.filter_by(group=group.id).all()
    g_dict = group.asdict()
    g_dict['questions'] = [q.asdict() for q in group.questions]
    g_dict['groups'] = []
    for group_id in group_ids:
        entry = Group.query.filter_by(id=group_id.entry).first()
        g_dict['groups'].append(get_group_tree(entry))
    return g_dict


@app.route('/v1/groups/<id>')
@secured('manager admin')
def group_get(token_data, id):
    group = Group.query.filter_by(id=id, user_id=token_data['id']).first()
    if not group:
        return http_err(404, 'group not found')
    return http_ok(**get_group_tree(group))

# @app.route('/v1/groups/<id>', methods=['DELETE'])
# @secured('manager admin')
# def group_delete(id, token_data):
#     group =