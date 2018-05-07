from testar import app, db
from testar.security import secured
from testar.utils import make_json, http_err, http_ok
from testar.models import Competition, User, Submission


@app.route('/v1/competitions/<id>/participants')
@secured('admin manager')
def participants_get(id, token_data):
    competition = Competition.query.filter_by(id=id, user_id=token_data['id']).first()
    if not competition:
        return http_err(404, 'competition not found')
    users = []
    for user in competition.participants:
        submission = [s.asdict() for s in Submission.query.filter_by(user_id=user.id, competition_id=competition.id).all()]
        user_dict = user.asdict()
        user_dict['submission'] = submission
        users.append(user_dict)
    return http_ok(participants=users)


@app.route('/v1/competitions/<id>/participants', methods=['POST'])
@secured('admin manager')
@make_json('users')
def participants_post(data, token_data, id):
    return 'todo'
    # competition = Competition.query.filter_by(id=id, user_id=token_data['id']).first()
    # if not competition:
    #     return http_err(404, 'competition not found')
    # if not isinstance(data['users'], list):
    #     return http_err(400, 'users must be array of (user id | username | email)')
    # unknown_ids = []
    # unknown_usernames = []
    # to_invite = []
    # added = []
    # for param in set(data['users']):
    #     if isinstance(param, int):
    #         user = User.query.get(param)
    #         if not user:
    #             unknown_ids.append(param)
    #             continue
    #         participant = Participant(user_id=user.id, competition_id=competition.id)
    #         competition.participants.append(participant)
    #         added.append(param)
    #     elif isinstance(param, str):
    #         if '@' in param:
    #             user = User.query.filter_by(email=param).first()
    #             if user:
    #                 participant = Participant(user_id=user.id, competition_id=competition.id)
    #                 competition.participants.append(participant)
    #                 added.append(param)
    #             else:
    #                 to_invite.append(param)
    #                 # TODO: user invitation
    #         else:
    #             user = User.query.filter_by(username=param).first()
    #             if not user:
    #                 unknown_usernames.append(param)
    #                 continue
    #             participant = Participant(user_id=user.id, competition_id=competition.id)
    #             competition.participants.append(participant)
    #             added.append(param)
    # if added:
    #     db.session.add(competition)
    #     db.session.commit()
    # resp = dict()
    # if unknown_usernames:
    #     resp['unknown_usernames'] = unknown_usernames
    # if unknown_ids:
    #     resp['unknown_ids'] = unknown_ids
    # if to_invite:
    #     resp['invited'] = to_invite
    # if added:
    #     resp['added'] = added
    # return http_ok(**resp)