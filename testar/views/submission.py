from testar import app
from testar import db
from testar.security import secured
from testar.models import User, Competition, Test, Submission, Answers
from testar.utils import http_err, http_ok, make_json
from time import time
from datetime import datetime


@app.route('/v1/competitions/<id>/test', methods=['GET'])
@secured()
def submissions_get(token_data, id):
    now = time()
    competition = Competition.query.get(id)
    if not competition:
        return http_err(404, 'competition not found')
    if competition.start_date > now:
        return http_err(404, "competition starts {}".format(datetime.fromtimestamp(competition.start_date)))
    if competition.end_date < now:
        return http_err(404, 'competition finished')
    test = Test.query.get(competition.test_id)
    if not test:
        return http_err(404, 'test not found')
    participant = User.query.get(token_data['id'])
    if participant not in competition.participants:
        competition.participants.append(participant)
        db.session.add(competition)
        db.session.commit()
    competition = competition.asdict()
    test_dict = test.asdict()
    test_dict['questions'] = test.mixed_questions()
    competition['test'] = test_dict
    return http_ok(**competition)


@app.route('/v1/competitions/<id>/submit', methods=['POST'])
@secured()
@make_json('questions')
def submission_post(id, data, token_data):
    if not isinstance(data['questions'], list):
        return http_err(400, 'questions must be array of dict', example=[dict(question=1, answer=4)])
    if not isinstance(data['questions'][0], dict):
        return http_err(400, 'questions must be array of dict', example=[dict(question=1, answer=4)])

    now = time()
    competition = Competition.query.get(id)
    if not competition:
        return http_err(404, 'competition not found')
    if competition.start_date > now:
        return http_err(404, "competition starts {}".format(datetime.fromtimestamp(competition.start_date)))
    if competition.end_date < now:
        return http_err(404, 'competition finished')

    participant = User.query.get(token_data['id'])
    if participant not in competition.participants:
        return http_err(403, 'you are not allowed to submit competition')
    test = Test.query.get(competition.test_id)
    if not test:
        return http_err(404, 'owner deleted the test')
    submitted = Submission.query.filter_by(user_id=participant.id, competition_id=competition.id).all()
    if submitted:
        return http_err(400, 'you have already submitted', submission=[s.asdict() for s in submitted])
    corrects = test.corrects()
    correct_count = 0
    for selected in data['questions']:
        if not selected.get('question') or 'answer' not in selected:
            return http_err(400, 'questions must be array of dict', example=[dict(question=1, answer=4)])
        if not corrects.get(selected['question']):
            return http_err(404, 'question not found', questions=selected)

        submission = Submission(question_id=selected['question'], answer_id=selected['answer'], user_id=participant.id,
                                competition_id=competition.id)
        db.session.add(submission)

        if selected['answer'] in corrects[selected['question']]:
            correct_count += 1
        selected['corrects'] = corrects[selected['question']]
    db.session.commit()
    return http_ok(corrects=correct_count, total=len(data['questions']))

