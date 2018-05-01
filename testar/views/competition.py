from testar import app, db
from testar.security import secured
from testar.utils import make_json, http_err, http_ok
from testar.models import Test, Competition, User, Participant


@app.route('/v1/competitions')
@secured()
def competitions_get(token_data):
    competitions = Competition.query.filter_by(user_id=token_data['id']).all()
    resp = [c.asdict() for c in competitions]
    return http_ok(competitions=resp)


@app.route('/v1/competitions/<id>')
@secured()
def competition_get(token_data, id):
    competition = Competition.query.filter_by(user_id=token_data['id'], id=id).first()
    if not competition:
        return http_err(404, 'competition not found')
    resp = competition.asdict()

    test = Test.query.get(competition.test_id)
    if not test:
        resp['test'] = 'not found'
    else:
        resp['test'] = test.asdict()

    return http_ok(**resp)


@app.route('/v1/competitions/<id>', methods=['PATCH'])
@secured()
@make_json()
def competition_patch(token_data, id, data):
    competition = Competition.query.filter_by(user_id=token_data['id'], id=id).first()
    if not competition:
        return http_err(404, 'competition not found')
    changed = False
    if data.get('test'):
        if not isinstance(data['test'], int):
            return http_err(400, 'test must be int (id of the test)')
        test = Test.query.filter_by(id=data['test'], owner=token_data['id']).first()
        if not test:
            return http_err(400, 'test not found')
        competition.test_id = test.id
        changed = True
    start = False
    end = False
    if data.get('start_date'):
        if not isinstance(data['start_date'], (int, float)):
            return http_err(400, 'start_date must be timestamp unix format')
        start = True
    if data.get('end_date'):
        if not isinstance(data['end_date'], (int, float)):
            return http_err(400, 'end_date must be timestamp unix format')
        end = True
    if start and end:
        if data['end_date'] < data['start_date']:
            return http_err(400, 'specify correct end_date *hint end_date must be greater than start_date')
        competition.start_date = data['start_date']
        competition.end_date = data['end_date']
        changed = True
    elif start:
        if competition.end_date < data['start_date']:
            return http_err(400, 'specify correct end_date *hint end_date must be greater than start_date')
        competition.start_date = data['start_date']
        changed = True
    elif end:
        if data['end_date'] < competition.start_date:
            return http_err(400, 'specify correct end_date *hint end_date must be greater than start_date')
        competition.end_date = data['end_date']
        changed = True

    if data.get('title'):
        if not isinstance(data['title'], str):
            return http_err(400, 'title must be string')
        competition.title = data['title']
        changed = True

    if data.get('description'):
        if not isinstance(data['description'], str):
            return http_err(400, 'description must be string')
        competition.description = data['description']
        changed = True
    if not changed:
        return http_err(400, 'there is no known parameters')
    db.session.add(competition)
    db.session.commit()
    return http_ok(**competition.asdict())


@app.route('/v1/competitions', methods=['POST'])
@secured()
@make_json('start_date', 'end_date', 'test', 'title')
def competitions_post(data, token_data):
    if not isinstance(data['start_date'], (int, float)):
        return http_err(400, 'start_date must be timestamp unix format')
    if not isinstance(data['end_date'], (int, float)):
        return http_err(400, 'end_date must be timestamp unix format')
    if data['end_date'] < data['start_date']:
        return http_err(400, 'specify correct end_date *hint greater than start_date')
    if not isinstance(data['test'], int):
        return http_err(400, 'test must be int (id of the test)')
    if not isinstance(data['title'], str):
        return http_err(400, 'title must be string')
    if data.get('description'):
        if not isinstance(data['description'], str):
            return http_err(400, 'description must be string')

    test = Test.query.filter_by(id=data['test'], owner=token_data['id']).first()
    if not test:
        return http_err(400, 'test not found')

    params = {
        k: v
        for k, v in data.items() if k in ['description', 'title', 'start_date', 'end_date']
    }
    competition = Competition(test_id=test.id, user_id=token_data['id'], **params)

    db.session.add(competition)
    db.session.commit()

    return http_ok(**competition.asdict())


@app.route('/v1/competitions/<id>/participants', methods=['POST'])
@secured()
@make_json('users')
def participants_post(data, token_data, id):
    competition = Competition.query.filter_by(id=id, user_id=token_data['id']).first()
    if not competition:
        return http_err(404, 'competition not found')
    if not isinstance(data['users'], list):
        return http_err(400, 'users must be array of (user id | username | email)')
    unknown_ids = []
    unknown_usernames = []
    to_invite = []
    added = []
    for param in set(data['users']):
        if isinstance(param, int):
            user = User.query.get(param)
            if not user:
                unknown_ids.append(param)
                continue
            participant = Participant(user_id=user.id, competition_id=competition.id)
            competition.participants.append(participant)
            added.append(param)
        elif isinstance(param, str):
            if '@' in param:
                user = User.query.filter_by(email=param).first()
                if user:
                    participant = Participant(user_id=user.id, competition_id=competition.id)
                    competition.participants.append(participant)
                    added.append(param)
                else:
                    to_invite.append(param)
                    # TODO: user invitation
            else:
                user = User.query.filter_by(username=param).first()
                if not user:
                    unknown_usernames.append(param)
                    continue
                participant = Participant(user_id=user.id, competition_id=competition.id)
                competition.participants.append(participant)
                added.append(param)
    if added:
        db.session.add(competition)
        db.session.commit()
    resp = dict()
    if unknown_usernames:
        resp['unknown_usernames'] = unknown_usernames
    if unknown_ids:
        resp['unknown_ids'] = unknown_ids
    if to_invite:
        resp['invited'] = to_invite
    if added:
        resp['added'] = added
    return http_ok(**resp)



