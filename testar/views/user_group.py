from testar import app, db
from testar.utils import http_ok, http_err, make_json
from testar.models import Group, User, GroupsGroups
from testar.security import secured
from flask import request


@app.route('/v1/user/groups', methods=['POST'])
@secured('admin manager')
@make_json('title')
def user_groups_post(data):
    if data.get('description'):
        if not isinstance(data['description'], str):
            return http_err(400, 'description parameter must be string')

        group = Group(title=data['title'], description=data['description'])
    else:
        group = Group(title=data['title'])
    if data.get('users'):
        if not isinstance(data['users'], list):
            return http_err(400, 'users parameter must be array')
        for u_id in data['users']:
            user = User.query.get(u_id)
            if not user:
                return http_err(404, 'user {} not found'.format(u_id))
            group.users.append(user)
    db.session.add(group)
    db.session.commit()
    return http_ok(**group.asdict())


@app.route('/v1/user/groups')
@secured('manager admin')
def user_groups_get():
    groups = Group.query.filter_by(user_id=None).all()
    groups = [g.asdict() for g in groups]
    return http_ok(groups=groups)


def get_group_tree(group):
    group_ids = GroupsGroups.query.filter_by(group=group.id).all()
    g_dict = group.asdict()
    g_dict['users'] = [q.asdict() for q in group.users]
    g_dict['groups'] = []
    for group_id in group_ids:
        entry = Group.query.filter_by(id=group_id.entry).first()
        g_dict['groups'].append(get_group_tree(entry))
    return g_dict


@app.route('/v1/user/groups/<id>')
@secured('manager admin')
def user_group_get(id):
    group = Group.query.filter_by(id=id, user_id=None).first()
    if not group:
        return http_err(404, 'group not found')
    return http_ok(**get_group_tree(group))


def group_available(id: int, entry: int):
    if id == entry:
        return False
    groups = GroupsGroups.query.filter_by(group=entry).all()
    for group in groups:
        if not group_available(id, group.entry):
            return False
    return True


@app.route('/v1/user/grouping', methods=['POST', 'DELETE'])
@secured('manager admin')
@make_json('group')
def user_grouping(data):
    if data.get('group'):
        if not isinstance(data['group'], int):
            return http_err(400, 'group must be int')
    else:
        return http_err(400, 'group parameter is missing')
    group = Group.query.filter_by(id=data['group'], user_id=None).first()
    if not group:
        return http_err(404, 'group not found')
    if data.get('users'):
        if not isinstance(data['users'], (int, list)):
            return http_err(400, 'users must be int or array, users id')
        if isinstance(data['users'], int):
            data['users'] = [data['users']]
        resp = []

        for u_id in data['users']:
            user = User.query.get(u_id)
            if not user:
                return http_err(404, 'user {} not found'.format(u_id))
            resp.append(user.asdict())
            if request.method == 'POST':
                if user not in group.users:
                    group.users.append(user)
            else:
                if user in group.users:
                    group.users.remove(user)

        db.session.add(group)
        db.session.commit()
        return http_ok(**group.asdict(), users=resp)

    if data.get('entry_group'):
        if not isinstance(data['entry_group'], (int, list)):
            return http_err(400, 'entry_group must be int or array')
        if isinstance(data['entry_group'], int):
            data['entry_group'] = [data['entry_group']]
        resp = []
        for g_id in data['entry_group']:
            entry_group = Group.query.filter_by(id=g_id, user_id=None).first()
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

    return http_err(400, 'users or entry_group parameter is missing')
